function goPage(pno, psize) //页号，每页展示行数
{   
    var itable = document.getElementById("table_result");//通过ID找到表格
    var num = itable.rows.length;//表格所有行数(所有记录数)
    var totalPage = 0;//总页数
    var pageSize = psize;//每页显示行数
    //总共分几页
    if (num / pageSize > parseInt(num / pageSize)) {
        totalPage = parseInt(num / pageSize) + 1;
    } else {
        totalPage = parseInt(num / pageSize);
    }
    var currentPage = pno;//当前页数
    var startRow = (currentPage - 1) * pageSize + 1;//开始显示的行  1
    var endRow = currentPage * pageSize;//结束显示的行   15
    endRow = (endRow > num) ? num : endRow;
    //遍历显示数据实现分页
    for (var i = 1; i < (num + 1); i++) {
        var irow = itable.rows[i - 1];
        if (i >= startRow && i <= endRow) {
            irow.style.display = "block";
        } else {
            irow.style.display = "none";
        }
    }
    var tempStr = "";
    if (currentPage > 1) {
        tempStr += "<a class=\"btn btn-ghost \" href=\"#\" onClick=\"goPage(" + (currentPage - 1) + "," + psize + ")\"><上一页</a>";
    }
    for (var j = 1; j < currentPage; j++) {
        tempStr += "<a class=\"btn btn-ghost\" href=\"#\" onClick=\"goPage(" + j + "," + psize + ")\">" + j + "</a>" ;
    }
    tempStr += "<a class=\"btn\">" + currentPage + "</a>" ;
    for (var j = currentPage+1; j <= totalPage; j++) {
        tempStr += "<a class=\"btn btn-ghost\" href=\"#\" onClick=\"goPage(" + j + "," + psize + ")\">" + j + "</a>" ;
    }
    if (currentPage < totalPage) {
        tempStr += "<a class=\"btn btn-ghost\"  href=\"#\" onClick=\"goPage(" + (currentPage + 1) + "," + psize + ")\">下一页></a>";
        
    }
    document.getElementById("barcon").innerHTML = tempStr;
}