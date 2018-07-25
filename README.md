#APIATUOTEST

1.接口自动化测试工具，通过case目录的yaml文件编写测试用例。

2.通过config文件夹配置邮箱，请求头，cookie,host，需要执行

的用例，case_no表示要执行的用例id用“,”隔开。

3.通过命令create templates生成测试文件夹,用例以及配置文件模板。

4.reports文件夹存储了每次执行的用例结果，以时间命名文件。

5.目前关联参数通过配置用例参数值为{id: 1001, value: group_id}表示需要从用例1001获

取参数group_id的值。

6.可通过数据库，message，status判断测试结果。

7.需要在create templates目录下执行命令api。


example:

    -
        name: 加入群
        method: GET
        hope: success
        url: api/group/join
        id: 1001
        params: {
            group_id: {id: 1002,value: group_id},
            user_id: 2
        }
    -
        name: 创建比赛
        method: POST
        type: file
        hope: sucess
        url: api/contest/store
        id: 1004
        params: {
            user_id: 3,
            video: '/home/hietel/PycharmProjects/APIAutoTest/config/some.txt',
            img: '/home/hietel/PycharmProjects/APIAutoTest/config/some.txt',
            group_id: {id: 1002,value: group_id},
            longitude: '113.9401565012',
            latitude: '22.5496157178',
            address: shenzhen,
            description: 'name',
            title: 'random',
            video_time: 20,
            }