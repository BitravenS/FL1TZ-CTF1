db = db.getSiblingDB("ctf_challenge");

db.users.insertOne({
  username: "admin",
  password: "FL1TZ{Y3S_1_No_sql_MangO!}"
});
