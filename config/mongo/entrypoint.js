db.createUser({user: "fluentd", pwd: "test", roles: [{ role: "readWrite", db: "fluentdb"}]});
db.createCollection("test");
