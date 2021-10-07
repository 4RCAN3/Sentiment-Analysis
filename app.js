const express = require("express");
const moment = require("moment");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const session = require("express-session");
const passport = require("passport");
const passportLocalMongoose = require("passport-local-mongoose")
const ejs = require("ejs");

const today = moment();

let currentDay =   today.format('YYYY-MM-DD')


const app = express();

app.use(
  session({
    secret: "My name is Ayush",
    resave: false,
    saveUninitialized: false,
  })
);

app.use(passport.initialize());
app.use(passport.session());

app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(express.static("public"));

mongoose.connect("mongodb://localhost:27017/someDB", { useNewUrlParser: true });

app.get("/", (req, res) => {
  
    res.render("sentiment", {currentDay : currentDay })
})

app.listen(5000, () => {
    console.log("Server Running on PORT 5000");
})
