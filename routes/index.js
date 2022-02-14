var express = require('express');
var router = express.Router();
const exec = require('child_process').exec;

function os_func() {
  this.execCommand = function(cmd, callback) {
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        return;
      }
      callback(stdout);
    });
  }
}
var os = new os_func();

/* GET home page. */
router.get('/', function(req, res, next) {

  os.execCommand('python3 smsblaster.py --get-sites', function(returnvalue) {
    sites = returnvalue.split('\n'); // convert to array
    sites.pop(); // 
    console.log(`Sites type: ${typeof(sites)}`);
    res.render('index', { 
      title: 'SMS BLASTER',
      sites: sites
    });    
  });

});

/* BLAST SMS MESSAGE */
router.post('/blast', function(req, res, next) {

  req.body.alertmessage
  req.body.sites

  if (Array.isArray(req.body.sites)) {
    req.body.sites.forEach(function(site) {
      console.log(`python3 smsblaster.py -m "${req.body.alertmessage}" -s ${site}`);
      os.execCommand(`python3 smsblaster.py -m "${req.body.alertmessage}" -s ${site}`, function(returnvalue) {
        console.log(returnvalue);
      });
    });
    res.send(`BLASTED customers for ${req.body.sites.length} sites!`);
  } else {
    console.log(`python3 smsblaster.py -m "${req.body.alertmessage}" -s ${req.body.sites}`);
    os.execCommand(`python3 smsblaster.py -m "${req.body.alertmessage}" -s ${req.body.sites}`, function(returnvalue) {
      console.log(returnvalue);
    });
    res.send(`BLASTED customers for 1 site!`);
  }
});

module.exports = router;
