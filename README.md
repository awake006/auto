#APIATUOTEST

1.Interface automation test tool, write test cases through the yaml file of the case directory.

2.Configure the mailbox through the config folder, request header, cookie, host, need to execute

The use case, case_no, indicates that the use case id to be executed is separated by ",".

3.Generate test folders, use cases, and configuration file templates with the command create templates.

4.The reports folder stores the use case results for each execution, naming the files by time.

5.Currently, the associated parameter parameter needs to be obtained from use case 1001 by setting the value of the use case parameter to {id: 1001, value: group_id}.

Take the value of the parameter group_id.

6.The test results can be judged through the database, message, status.

7.You need to execute the command api in the create templates directory.


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