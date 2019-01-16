var mysql = require('mysql');
var config = require('./config.json');
var pool = mysql.createPool ({
    host      :       //endpoint,
    user      :       //username,
    password  :       //password,
    database  :       //db_name

})

function insertField (queryString, connection, callback) {
    // console.log("INSERT START");
    connection.query(queryString, function (err, results, fields) {
        // console.log("in insert")
        if (err) {
            // console.log("insert error");
            callback(err, null);
        } else {
            // console.log("blah");
            callback(null, "Successful entry");
        }
    })
}


function selectQuery (queryString, connection, callback) {

    connection.query(queryString, function(err, results, fields) {
        if (err) {
            callback(err, null);
        } else {
            if (results.length == 0) {
                callback(null, null);
            } else {   
                callback(null, results);
            }
            
        }
    });
}

function insertData(callback, connection, fields) {
    var lat = fields.lat; 
    var long = fields.long; 
    var dangerRating = fields.dangerRating; 
    
    var queryString = "INSERT INTO bike_db_schema.DangerData (latitude, longitude, dangerRating) VALUES (" +  lat + ", " + long + ", " + dangerRating + ")";
    insertField(queryString, connection, callback); 
}

function getAllDAta(callback, connection) {
    var queryString = "SELECT * FROM bike_db_schema.DangerData"; 
    selectQuery(queryString, connection, callback); 
}


exports.handler = (event, context, callback) => {
    context.callbackWaitsForEmptyEventLoop = false; 
    pool.getConnection(function(err, connection) {
        if (err) {
            callback(err); 
        } 
        
        else {
            var action = event.action; 
            var fields = event.fields; 
    
            switch(action) {
                case "insert":
                    insertData(callback, connection, fields); 
                    break;
                case "get":
                    getAllDAta(callback, connection);
                    break; 
            }
        }
    });
}
