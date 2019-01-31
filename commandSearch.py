def parseCommand(command,brand):
    allowed_opt = ['title', 'brand', 'language','site','name']
    command_dict = {}
    opt = 'contents'
    q=command.split()
    try:
	high=float(str(q[-1]))
	q.pop()
    except:
	high=99999
    try:
	low=float(str(q[-1]))
	q.pop()
    except:
	low=0
    if brand!="1":
        command_dict['brand']=command_dict.get('brand', '') + ' ' + brand
    for i in q:
        if ':' in i:
	   
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            lis=jieba.cut(i)
	    for j in lis:
	        command_dict[opt] = command_dict.get(opt, '') + ' ' + j
    return command_dict,low,high


def Run_Price(searcher_good, searcher_bad, analyzer, command, brand):
    while True:
        command_dict,low,high = parseCommand(command, brand)
	total_num=20

	s=SortField("price",SortField.Type.FLOAT,False)
	#s=SortField("total_comment",SortField.Type.FLOAT,True)
	#s=SortField("good_rate",SortField.Type.FLOAT,True)
	#s=SortField("socre",SortField.Type.FLOAT,True)
	so=Sort(s)
        querys = BooleanQuery()
        for k,v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k,
                              analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)

        #The price's range
	q=NumericRangeQuery.newFloatRange("price",low,high,True,True)
	querys.add(q,BooleanClause.Occur.MUST)
	
        scoreDocs_good = searcher_good.search(querys, total_num,so).scoreDocs
	total=len(scoreDocs_good)
	flag=True
	if len(scoreDocs_good)<total_num:
	    scoreDocs_bad = searcher_bad.search(querys, total_num,so).scoreDocs
	    total=total+len(scoreDocs_bad)
	    flag=False
	if total>total_num:
	    total=total_num
        #Total is the number of matched websites
	res = []
        for scoreDoc_good in scoreDocs_good:
	    unit = []
            doc = searcher_good.doc(scoreDoc_good.doc)
            title = doc.get('title')
	    title.replace(' ', '')
	    title = title[:18]
            total_comment = doc.get("total_comment")
	    price = doc.get("price")
	    socre = doc.get("socre")
	    brand = doc.get("brand")
	    good_rate = doc.get("good_rate")
	    url = doc.get("url")
	    img_url = doc.get("img_url")
	    comment = doc.get("comment").split()
	    unit.append(title)             #0
	    unit.append(total_comment)     #1
	    unit.append(price)             #2
	    unit.append(socre)		   #3
	    unit.append(brand)		   #4
	    unit.append(good_rate)	   #5
	    unit.append(url)		   #6
	    unit.append(img_url)	   #7
	    unit.append(comment) 	   #8
	    res.append(unit)		  
	if not flag:
	    t=0
	    for scoreDoc_bad in scoreDocs_bad:
		t=t+1
                doc = searcher_bad.doc(scoreDoc_bad.doc)
##                explanation = searcher.explain(query, scoreDoc.doc)
                title = doc.get('title')
		title.replace(' ', '')
           	title = title[:18]
                total_comment = doc.get("total_comment")
	        price = doc.get("price")
	        socre = doc.get("socre")
	        brand = doc.get("brand")
	        good_rate = doc.get("good_rate")
		url = doc.get("url")
                img_url = doc.get("img_url")
		comment = doc.get("comment").split()
	        unit.append(title)
	    	unit.append(total_comment)
	    	unit.append(price)
	    	unit.append(socre)
	    	unit.append(brand)
	    	unit.append(good_rate)
		unit.append(url)
		unit.append(img_url)
		unit.append(comment)
	    	res.append(unit)
		if t>total_num-1-len(scoreDocs_good):
		    break
	res.append(brand)
	return res


def Run_TotalComment(searcher_good, searcher_bad, analyzer, command, brand):
    while True:
        command_dict,low,high = parseCommand(command, brand)
	total_num=20

	#s=SortField("price",SortField.Type.FLOAT,False)
	s=SortField("total_comment",SortField.Type.FLOAT,True)
	#s=SortField("good_rate",SortField.Type.FLOAT,True)
	#s=SortField("socre",SortField.Type.FLOAT,True)
	so=Sort(s)

        querys = BooleanQuery()
        for k,v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k,
                              analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)

        #The price's range
	q=NumericRangeQuery.newFloatRange("price",low,high,True,True)
	querys.add(q,BooleanClause.Occur.MUST)
	
        scoreDocs_good = searcher_good.search(querys, total_num,so).scoreDocs
	total=len(scoreDocs_good)
	flag=True
	if len(scoreDocs_good)<total_num:
	    scoreDocs_bad = searcher_bad.search(querys, total_num,so).scoreDocs
	    total=total+len(scoreDocs_bad)
	    flag=False
	if total>total_num:
	    total=total_num
        #Total is the number of matched websites
	res = []
        for scoreDoc_good in scoreDocs_good:
	    unit = []
            doc = searcher_good.doc(scoreDoc_good.doc)
            title = doc.get('title')
	    title.replace(' ', '')
	    title = title[:18]
            total_comment = doc.get("total_comment")
	    price = doc.get("price")
	    socre = doc.get("socre")
	    brand = doc.get("brand")
	    good_rate = doc.get("good_rate")
	    url = doc.get("url")
	    img_url = doc.get("img_url")
	    comment = doc.get("comment").split()
	    unit.append(title)             #0
	    unit.append(total_comment)     #1
	    unit.append(price)             #2
	    unit.append(socre)		   #3
	    unit.append(brand)		   #4
	    unit.append(good_rate)	   #5
	    unit.append(url)		   #6
	    unit.append(img_url)	   #7
	    unit.append(comment)	   #8
	    res.append(unit)		  
	if not flag:
	    t=0
	    for scoreDoc_bad in scoreDocs_bad:
		t=t+1
                doc = searcher_bad.doc(scoreDoc_bad.doc)
##                explanation = searcher.explain(query, scoreDoc.doc)
                title = doc.get('title')
		title.replace(' ', '')
           	title = title[:18]
                total_comment = doc.get("total_comment")
	        price = doc.get("price")
	        socre = doc.get("socre")
	        brand = doc.get("brand")
	        good_rate = doc.get("good_rate")
		url = doc.get("url")
                img_url = doc.get("img_url")
		comment = doc.get("comment").split()
	        unit.append(title)
	    	unit.append(total_comment)
	    	unit.append(price)
	    	unit.append(socre)
	    	unit.append(brand)
	    	unit.append(good_rate)
		unit.append(url)
		unit.append(img_url)
		unit.append(comment)
	    	res.append(unit)
		if t>total_num-1-len(scoreDocs_good):
		    break
	res.append(brand)
	return res


def Run_GoodRate(searcher_good, searcher_bad, analyzer, command, brand):
    while True:
        command_dict,low,high = parseCommand(command, brand)
	total_num=20

	#s=SortField("price",SortField.Type.FLOAT,False)
	#s=SortField("total_comment",SortField.Type.FLOAT,True)
	s=SortField("good_rate",SortField.Type.FLOAT,True)
	#s=SortField("socre",SortField.Type.FLOAT,True)
	so=Sort(s)

        querys = BooleanQuery()
        for k,v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k,
                              analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)

        #The price's range
	q=NumericRangeQuery.newFloatRange("price",low,high,True,True)
	querys.add(q,BooleanClause.Occur.MUST)
	
        scoreDocs_good = searcher_good.search(querys, total_num,so).scoreDocs
	total=len(scoreDocs_good)
	flag=True
	if len(scoreDocs_good)<total_num:
	    scoreDocs_bad = searcher_bad.search(querys, total_num,so).scoreDocs
	    total=total+len(scoreDocs_bad)
	    flag=False
	if total>total_num:
	    total=total_num
        #Total is the number of matched websites
	res = []
        for scoreDoc_good in scoreDocs_good:
	    unit = []
            doc = searcher_good.doc(scoreDoc_good.doc)
##            explanation = searcher.explain(query, scoreDoc.doc) ???
            title = doc.get('title')
	    title.replace(' ', '')
	    title = title[:18]
            total_comment = doc.get("total_comment")
	    price = doc.get("price")
	    socre = doc.get("socre")
	    brand = doc.get("brand")
	    good_rate = doc.get("good_rate")
	    url = doc.get("url")
	    img_url = doc.get("img_url")
	    comment = doc.get("comment").split()
	    unit.append(title)             #0
	    unit.append(total_comment)     #1
	    unit.append(price)             #2
	    unit.append(socre)		   #3
	    unit.append(brand)		   #4
	    unit.append(good_rate)	   #5
	    unit.append(url)		   #6
	    unit.append(img_url)	   #7
	    unit.append(comment)	   #8
	    res.append(unit)		  
	if not flag:
	    t=0
	    for scoreDoc_bad in scoreDocs_bad:
		t=t+1
                doc = searcher_bad.doc(scoreDoc_bad.doc)
##                explanation = searcher.explain(query, scoreDoc.doc)
                title = doc.get('title')
		title.replace(' ', '')
           	title = title[:18]
                total_comment = doc.get("total_comment")
	        price = doc.get("price")
	        socre = doc.get("socre")
	        brand = doc.get("brand")
	        good_rate = doc.get("good_rate")
		url = doc.get("url")
                img_url = doc.get("img_url")
		comment = doc.get("comment").split()
	        unit.append(title)
	    	unit.append(total_comment)
	    	unit.append(price)
	    	unit.append(socre)
	    	unit.append(brand)
	    	unit.append(good_rate)
		unit.append(comment)
		unit.append(url)
		unit.append(img_url)
	    	res.append(unit)
		if t>total_num-1-len(scoreDocs_good):
	       	    break
	res.append(brand)
	return res


def Run_Score(searcher_good, searcher_bad, analyzer, command, brand):
    while True:
        command_dict,low,high = parseCommand(command,brand)
	total_num=20

	#s=SortField("price",SortField.Type.FLOAT,False)
	#s=SortField("total_comment",SortField.Type.FLOAT,True)
	#s=SortField("good_rate",SortField.Type.FLOAT,True)
	s=SortField("socre",SortField.Type.FLOAT,True)
	so=Sort(s)

        querys = BooleanQuery()
        for k,v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k, analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)

        #The price's range
	q=NumericRangeQuery.newFloatRange("price",low,high,True,True)
	querys.add(q,BooleanClause.Occur.MUST)
	
        scoreDocs_good = searcher_good.search(querys, total_num,so).scoreDocs
	total=len(scoreDocs_good)
	flag=True
	if len(scoreDocs_good)<total_num:
	    scoreDocs_bad = searcher_bad.search(querys, total_num,so).scoreDocs
	    total=total+len(scoreDocs_bad)
	    flag=False
	if total>total_num:
	    total=total_num
        #Total is the number of matched websites
	res = []
        for scoreDoc_good in scoreDocs_good:
	    unit = []
            doc = searcher_good.doc(scoreDoc_good.doc)
##            explanation = searcher.explain(query, scoreDoc.doc) ???
            title = doc.get('title')
	    title.replace(' ', '')
	    title = title[:18]
            total_comment = doc.get("total_comment")
	    price = doc.get("price")
	    socre = doc.get("socre")
	    brand = doc.get("brand")
	    good_rate = doc.get("good_rate")
	    url = doc.get("url")
	    img_url = doc.get("img_url")
	    comment = doc.get("comment").split()
	    unit.append(title)             #0
	    unit.append(total_comment)     #1
	    unit.append(price)             #2
	    unit.append(socre)		   #3
	    unit.append(brand)		   #4
	    unit.append(good_rate)	   #5
	    unit.append(url)		   #6
	    unit.append(img_url)	   #7
	    unit.append(comment)
	    res.append(unit)		  
	if not flag:
	    t=0
	    for scoreDoc_bad in scoreDocs_bad:
		t=t+1
                doc = searcher_bad.doc(scoreDoc_bad.doc)
##                explanation = searcher.explain(query, scoreDoc.doc)
                title = doc.get('title')
		title.replace(' ', '')
           	title = title[:18]
                total_comment = doc.get("total_comment")
	        price = doc.get("price")
	        socre = doc.get("socre")
	        brand = doc.get("brand")
	        good_rate = doc.get("good_rate")
		url = doc.get("url")
                img_url = doc.get("img_url")
		comment = doc.get("comment").split()
	        unit.append(title)
	    	unit.append(total_comment)
	    	unit.append(price)
	    	unit.append(socre)
	    	unit.append(brand)
	    	unit.append(good_rate)
		unit.append(url)
		unit.append(img_url)
		unit.append(comment)
	    	res.append(unit)
		if t>total_num-1-len(scoreDocs_good):
		    break
	res.append(brand)
	return res




def SortByScore(command):
    STORE_DIR_GOOD = "index_good"
    STORE_DIR_BAD = "index_bad"
    vm_env.attachCurrentThread()
    directory_good = SimpleFSDirectory(File(STORE_DIR_GOOD))
    searcher_good = IndexSearcher(DirectoryReader.open(directory_good))
    directory_bad = SimpleFSDirectory(File(STORE_DIR_BAD))
    searcher_bad = IndexSearcher(DirectoryReader.open(directory_bad))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        #command=command+u' '+u'brand:'+xx.decode('utf8')
    res = Run_Score(searcher_good, searcher_bad, analyzer, command, user_data.brand)
    return res

def SortByPrice(self, name):
    STORE_DIR_GOOD = "index_good"
    STORE_DIR_BAD = "index_bad"
    vm_env.attachCurrentThread()
    directory_good = SimpleFSDirectory(File(STORE_DIR_GOOD))
    searcher_good = IndexSearcher(DirectoryReader.open(directory_good))
    directory_bad = SimpleFSDirectory(File(STORE_DIR_BAD))
    searcher_bad = IndexSearcher(DirectoryReader.open(directory_bad))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    res = Run_Price(searcher_good, searcher_bad, analyzer, command, user_data.brand)
    return res


def SortByHo(command):
    STORE_DIR_GOOD = "index_good"
    STORE_DIR_BAD = "index_bad"
    vm_env.attachCurrentThread()
    directory_good = SimpleFSDirectory(File(STORE_DIR_GOOD))
    searcher_good = IndexSearcher(DirectoryReader.open(directory_good))
    directory_bad = SimpleFSDirectory(File(STORE_DIR_BAD))
    searcher_bad = IndexSearcher(DirectoryReader.open(directory_bad))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    res = Run_TotalComment(searcher_good, searcher_bad, analyzer, command, user_data.brand)
    return res

def SortByGood(command):
    STORE_DIR_GOOD = "index_good"
    STORE_DIR_BAD = "index_bad"
    vm_env.attachCurrentThread()
    directory_good = SimpleFSDirectory(File(STORE_DIR_GOOD))
    searcher_good = IndexSearcher(DirectoryReader.open(directory_good))
    directory_bad = SimpleFSDirectory(File(STORE_DIR_BAD))
    searcher_bad = IndexSearcher(DirectoryReader.open(directory_bad))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    res = Run_GoodRate(searcher_good, searcher_bad, analyzer, command, user_data.brand)
    return res

class GetComments:
    def GET(self, name):
	STORE_DIR_GOOD = "index_good"
	STORE_DIR_BAD = "index_bad"
        vm_env.attachCurrentThread()
        directory_good = SimpleFSDirectory(File(STORE_DIR_GOOD))
        searcher_good = IndexSearcher(DirectoryReader.open(directory_good))
	directory_bad = SimpleFSDirectory(File(STORE_DIR_BAD))
        searcher_bad = IndexSearcher(DirectoryReader.open(directory_bad))
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
	user_data = web.input(name = None)
        command = yourInput(user_data)
	if user_data.brand == '':
	    user_data.brand = '1'
	res = Run_Score(searcher_good, searcher_bad, analyzer, name, user_data.brand)
	comments = []
	for i in range(len(res)):
	    if len(res[i])==9:
	        t = res[i][8]
	    else:
		t = ''
	    for j in range(len(t)):
		s = t[j]
	        s.encode("utf8")
		if len(s) >= 50:
    	    	    comments.append(s)
        return render.comments(comments)
