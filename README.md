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
        name: get request
        method: GET
        chenk_method: db  Verify that the request parameters are consistent with the results stored in the database
        sql: select * from table where img_id=%s,img_id
        url: api/get/example
        id: 1001
        params:
            img_id:
            id: 1002  Get img_id from the use case result with case_id of 1002
            value: img_id

    - 
        name: post request
        method: POST
        type: file
        chenk_method: db  
        sql: select * from table where contest_id=100 
        url: api/post/example
        id: 1001
        params:
            contest_id: 100
            address: shenzhen
            description: str,20 (a string of length 20)
            title: random (random number does not repeat)
            video_time: 20
            img_id:
            id: 1002  
            value: img_id

    - 
        name: upload file
        method: POST
        type: file  File upload identifier, when not empty, indicates that the use case is a file upload
        chenk_method: message  Verify that the value of the return value is success
        message: sucess
        url: api/upload/file
        id: 1002
        params:
            name: random
            img: file abspath

    -
        name: put request
        method: PUT
        chenk_method: message
        message: success
        url: api/put/example/%s,img_id
        id: 1003
        params:
        contest_id: 100
        address: shenzhen
        description: str,20 
        title: random 
        video_time: 20
        img_id:
            id: 1002 
            value: img_id
    - 
        name: delete request
        method: delete
        chenk_method: message
        message: success
        url: api/delete/example/%s,img_id
        id: 1004
        params:
        contest_id: 100
        address: shenzhen
        description: str,20
        title: random
        video_time: 20
        img_id:
            id: 1002 
            value: img_id
