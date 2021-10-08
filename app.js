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

const MONGODB_URI = "mongodb+srv://AyushKatoch:ayush2002@cluster0.nj2xk.mongodb.net/shop?retryWrites=true&w=majority";

mongoose.connect(MONGODB_URI , { useNewUrlParser: true });

const realDataSchema = new mongoose.Schema({
  name: String,
  historicalData : String,
  historicalDataDate: Date,
  popularTweet: String,
  popularTweetNum: Number
});

const StatModel = new mongoose.model("StatModel", realDataSchema);

app.get("/", (req, res) => {
  
    res.render("sentiment", {currentDay : currentDay })
})

app.post("/", (req, res, next) => {
  const statModel = new StatModel({
  name: req.body.realTimeData,
  historicalData : req.body.historicalData,
  historicalDataDate: req.body.historicalDataDate,
  popularTweet: req.body.popularTweet,
  popularTweetNum: req.body.popularTweetNum

})
  statModel.save().then(result => {
    console.log(result);
  }).catch(err => {
    console.log(err);
  })
  res.redirect("/");
})

app.listen(5000, () => {
    console.log("Server Running on PORT 5000");
})
