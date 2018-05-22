#APIATUOTEST

1.接口自动化测试工具，通过case目录的yaml文件编写测试用例。

2.通过config文件夹配置邮箱，请求头，cookie,host，需要执行

的用例，number表示要执行的用例id用“,”隔开。

3.reports文件夹存储了每次执行的用例结果，以时间命名文件。

4.common文件夹为辅助方法。

5.目前关联参数通过配置用例参数值为{id: 1001, value: group_id}表示需要从用例1001获

取参数group_id的值。

6.通过判断用例中的hope参数是否与实际结果一致来验证。

7.需要在当前文件夹下执行run.py。

8.yaml的type为file时表示是文件上传类型的接口，不填或填其他表示普通数据的请求。


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