# coding=utf8
from app import db

def get_databases():
	sql = "SHOW DATABASES"
	result = db.engine.execute(sql)
	dbs = []
	for row in result:
		dbs.append(row['Database'])
	return dbs

def get_tables(dbname):
	sql = "SELECT TABLE_NAME AS tableName FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='" + dbname + "'"
	result = db.engine.execute(sql)
	tables = []
	for row in result:
		tables.append(row['tableName'])
	return tables

def get_table_field(tablename):
	sql = "SHOW FULL COLUMNS FROM " + tablename
	results = db.engine.execute(sql)
	fields = []
	for result in results:
		fields.append({'field': result['Field'], 'type': result['Type'], \
					   'isNull': result['Null'], 'key': result['Key'], \
					   'defaultValue': result['Default'], 'extra': result['Extra'], 'comment': result['Comment']})
	return fields

def get_select_field(tableName, fields):
	sql = "SELECT "
	sqlField = ""
	for field in fields:
		attr = convertField(field['field'])
		if (sqlField == ''):
			sqlField += field['field']
		else:
			sqlField += ',' + field['field']
	sql += sqlField + ' FROM ' + tableName
	return sql

def get_insert_sql(objectName, tableName, fields):
	sql = "INSERT INTO " + tableName + " "
	sqlField = ''
	sqlValue = ''
	for field in fields:
		if (field['extra'] != 'auto_increment'):
			if (sqlField == ''):
				sqlField += field['field']
			else:
				sqlField += ',' + field['field']
	sql += '(' + sqlField + ') VALUES '

	for field in fields:
		if (field['extra'] != 'auto_increment'):
			attr = convertField(field['field'])
			if (sqlValue == ''):
				sqlValue = '#{' + attr + '}'
			else:
				sqlValue += ',#{' + attr + '}'
	sql += '(' + sqlValue + ') '
	return sql

def get_update_sql(objectName, tableName, fields):
	sql = "UPDATE " + tableName + " SET "
	sqlField = ""
	where = ""
	for field in fields:
		attr = convertField(field['field'])
		if (field['extra'] != 'auto_increment'):
			if (sqlField == ''):
				sqlField += field['field'] + '=#{' + attr + '}'
			else:
				sqlField += ', ' + field['field'] + '=#{' + attr + '}'
		if (field['extra'] == 'auto_increment'):
			where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
	sql += sqlField + where
	return sql

def get_update_sql_v2(tableName, fields):
	sql = "UPDATE " + tableName + "<br/>"
	sql += "\t\t&lt;set&gt;<br/>"
	for field in fields:
		attr = convertField(field['field'])
		if not (field['extra'] == 'auto_increment'):
			sql += "\t\t\t&lt;if test=\"" + attr + "!=null\"&gt; " + field['field'] + "=#{" + attr + "} " \
																									 "&lt;/if&gt;<br/>"
	sql += "\t\t&lt;/set&gt;<br/>"
	sql += "\t\tWHERE id=#{id}"
	return sql

def get_delete_sql(objectName, tableName, fields):
	sql = "DELETE FROM " + tableName
	where = ""
	for field in fields:
		attr = convertField(field['field'])
		if (field['extra'] == 'auto_increment'):
			where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
	sql += where
	return sql

def get_select_sql(tableName, fields):
	sql = "SELECT "
	sqlField = ""
	where = ""
	for field in fields:
		attr = convertField(field['field'])
		if (sqlField == ''):
			sqlField += field['field'] + ' AS ' + attr
		else:
			sqlField += ',' + field['field'] + ' AS ' + attr
		if (field['extra'] == 'auto_increment'):
			where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
	sql += sqlField + ' FROM ' + tableName + where
	return sql

def get_simple_select_sql(tableName, fields):
	sql = "SELECT "
	sqlField = ""
	where = ""
	for field in fields:
		attr = convertField(field['field'])
		if (sqlField == ''):
			sqlField += field['field']
		else:
			sqlField += ',' + field['field']
		if (field['extra'] == 'auto_increment'):
			where = ' WHERE ' + field['field'] + '=#{' + attr + '}'
	sql += sqlField + ' FROM ' + tableName + where
	return sql

def get_java_code(objectName, fields):
	code = "public class " + titleFirst(objectName) + " {<br/>"
	for field in fields:
		attr = convertField(field['field'])
		code += "\t" + '/** ' + field['comment'] + '*/' + "<br/>"
		code += "\t" + 'private String ' + attr + ";<br/>"
	code += '}';
	return code

def get_mybatis_xml(objectName, tableName, fields):
	select_fileds = get_select_field(tableName, fields)
	simple_select_sql = get_simple_select_sql(tableName, fields)
	insert_sql = get_insert_sql(objectName, tableName, fields)
	update_sql = get_update_sql(objectName, tableName, fields)
	#update_sql_v2 = get_update_sql_v2(tableName, fields)
	className = titleFirst(objectName)
	code = ""

	code += "&lt;?xml version=\"1.0\" encoding=\"UTF-8\" ?&gt;<br/>"
	code += "&lt;!DOCTYPE mapper PUBLIC \"-//mybatis.org//DTD Mapper 3.0//EN\" " \
			"\"http://mybatis.org/dtd/mybatis-3-mapper.dtd\"&gt;<br/>"

	code += "&lt;mapper namespace=\"" + className + "Mapper\"&gt;<br/>"
	code += "\t&lt;resultMap id=\"" + objectName + "Map\" type=\"" + className + "\"&gt;<br />"
	for field in fields:
		attr = convertField(field['field'])
		code += "\t\t&lt;id column=\"" + field['field'] + "\" property=\"" + attr + "\" /&gt;<br/>"
	code += "\t&lt;/resultMap&gt;<br/><br/>"

	# Select fields
	code += "\t&lt;sql id=\"selectFields\"&gt;<br/>"
	code += "\t\t" + select_fileds + "<br/>"
	code += "\t&lt;/sql&gt;<br/><br/>"

	# Select by id SQL
	code += "\t&lt;select id=\"get" + className + "ById\" resultMap=\"" + objectName + "Map\"&gt;<br/>"
	code += "\t\t&lt;include refid=\"selectFields\" /&gt;<br/>"
	code += "\t\tWHERE id=#{id}<br/>"
	code += "\t&lt;/select&gt;<br/><br/>"

	# Select all SQL
	code += "\t&lt;select id=\"get" + className + "s\" resultMap=\"" + objectName + "Map\"&gt;<br/>"
	code += "\t\t&lt;include refid=\"selectFields\" /&gt;<br/>"
	code += "\t\tORDER BY id DESC<br/>"
	code += "\t&lt;/select&gt;<br/><br/>"

	# Create SQL
	code += "\t&lt;insert id=\"create" + className + "\" useGeneratedKeys=\"true\" keyProperty=\"id\" " \
													 "parameterType=\"" + className + "\"&gt;<br/>"
	code += "\t\t" + insert_sql + "<br/>"
	code += "\t&lt;/insert&gt;<br/><br/>"
	# Update SQL
	code += "\t&lt;update id=\"update" + className + "\" parameterType=\"" + className + "\"&gt;<br/>"
	code += "\t\t" + update_sql + "<br/>"
	code += "\t&lt;/update&gt;<br/><br/>"

	# Update SQL V2
	#code += "\t&lt;update id=\"update" + className + "\" parameterType=\"" + className + "\"&gt;<br/>"
	#code += "\t\t" + update_sql_v2 + "<br/>"
	#code += "\t&lt;/update&gt;<br/><br/>"

	# Delete SQL
	code += "\t&lt;delete id=\"delete" + className + "\" parameterType=\"int\"&gt;<br/>"
	code += "\t\tDELETE FROM " + tableName + " WHERE id=#{id}<br/>"
	code += "\t&lt;/delete&gt;<br/>"

	code += "&lt;/mapper&gt;<br/>"
	return code

def getJavaMapper(objectName):
	className = titleFirst(objectName)
	code = "public interface " + className + "Mapper {<br/>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * &lt;pre&gt;&lt;/pre&gt;' + "<br/>"
	code += "\t" + ' * @param ' + objectName + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public int create' + className + '(' + className + ' '+objectName+');' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param ' + objectName + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public int update' + className + '(' + className + ' '+objectName+');' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param id' + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public int delete' + className + '(@Param("id") int id);' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param id' + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public ' + className + ' get' + className + 'ById(@Param("id") int id);' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param ' + objectName + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public List&lt;' + className + '&gt; get' + className + 's();' + "<br/>"

	code += '}';
	return code

def getJavaService(objectName):
	className = titleFirst(objectName)
	code = "public interface " + className + "Service {<br/>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param ' + objectName + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public int create' + className + '(' + className + ' '+objectName+');' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param ' + objectName + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public int update' + className + '(' + className + ' '+objectName+');' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param '+objectName+'Id' + "<br/>"
	code += "\t" + ' * @return int' + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public int delete' + className + '(int '+objectName+'Id);' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param '+objectName+'Id' + "<br/>"
	code += "\t" + ' * @return ' + className + "<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public ' + className + ' get' + className + 'ById(int '+objectName+'Id);' + "<br/>"

	code += "<br>"

	code += "\t" + '/**' + "<br/>"
	code += "\t" + ' * @param ' + objectName + "<br/>"
	code += "\t" + ' * @return List&lt;' + className + '&gt;'+"<br/>"
	code += "\t" + ' */' + "<br/>"
	code += "\t"+ 'public List&lt;' + className + '&gt; get' + className + 's();' + "<br/>"

	code += '}';
	return code

def convertField(field):
	fieldList = field.split("_")
	attr = ''
	for f in fieldList:
		if (attr == ''):
			attr = f
		else:
			attr += f.title()
	return attr

def titleFirst(str):
	if len(str)<=0:
		return
	return str[0:1].title() + str[1:]

def debug_print(msg):
	print "\n##########################################################################################################"
	print msg
	print "\n##########################################################################################################"