function range(data){
    index = []
    for (var i=0; i<=data.length-1; i++) {
        index.push(i)
    }
    return index
}
function drawLine(id,data,title,subtext) {
    var myChart=echarts.init(document.getElementById(id))
    option = {
        title : {
            text: title,
            subtext: subtext
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['意向']
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : range(data)
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name: title,
                type:'line',
                smooth:true,
                itemStyle: {normal: {areaStyle: {type: 'default'}}},
                data: data
            }
        ]
    };
    myChart.setOption(option);
}
function success(data) {
    console.log(data)
    cpu=[]
    memory=[]
    disk=[]
    network=[]
    for (var i=0;i<data['data'].length;i++){
        cpu.push(data['data'][i]['cpu']['avg'])
        cpu.push(data['data'][i]['memory']['percent'])
        disk.push(data['data'][i]['disk']['percent'])
        network.push(data['data'][i]['network']['packets']['sent'])
    }
    drawLine('cpu',cpu,"处理器","使用率")
    drawLine('memory',memory,"内存","使用率")
    drawLine('dis',disk,"硬盘","使用率")
    drawLine('network',network,'网卡','发送')

}
function fail(data) {
    console.log(data)
}
function search() {
    var url="http://127.0.0.1:5000/monitor/api/v1/search"
    data={
        'ip':$('#ip').val(),
        'start':$('#start').datetimepicker('getFormattedDate'),
        'end':$('#end').datetimepicker('getFormattedDate')
    }
    console.log(data)
    http(url,data,'GET',success,fail)
}

function init_datetimepicker() {
    $('#start').datatimepicker({
        autoclose:true
        format: 'yyyy-mm-dd hh:ii:ss',
        minView: 0,  //0表示可以选择小时、分钟   1只可以选择小时
        minuteStep:1 //分钟间隔1分钟
    });
    $('#start').datetimepicker('update', new Date());
    $('#end').datetimepicker({
        autoclose : true,
        format: 'yyyy-mm-dd hh:ii:ss',
        minView:0,  //0表示可以选择小时、分钟   1只可以选择小时
        minuteStep:1 //分钟间隔1分钟
    });
    $('#end').datetimepicker('update', new Date());

}
function get_ip_list() {
    var url = host + "/monitor/api/v1/ip/list"
    http(url, {}, 'GET', function(data){
        var html = "";
        for (index in data['data']) {
            ip = data['data'][index]
            html += '<option value="' + ip + '">' + ip + '</option>'
        }
        $('#ip').append(html)
    }, function(data){
        console.log(data)
    })
}

$(function() {
    init_datetimepicker();
    get_ip_list();
    $('#search').click(search);
})