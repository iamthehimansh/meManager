const Imap = require('node-imap');
const { simpleParser } = require('mailparser');
// const fetch = require('node-fetch'); // Assuming you're using node-fetch for the HTTP request
// const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const axios = require('axios');

const url = 'http://127.0.0.1:5000';
const imap = new Imap({
  user: process.env.EMAIL,
  password: process.env.PASSWORD,
  host: 'imap.gmail.com',
  port: 993,
  tls: true,
  tlsOptions: { rejectUnauthorized: false },
});

function openInbox(cb) {
  imap.openBox('INBOX', false, cb);
}

imap.once('ready', function () {
  openInbox(function (err, box) {
    if (err) throw err;
    console.log('Connected to inbox!');

    imap.on('mail', function (numNewMsgs) {
      console.log(`${numNewMsgs} new email(s) arrived.`);
      imap.search(['UNSEEN'], function (err, results) {
        if (err) throw err;

        if (results.length === 0) {
          console.log('No new unseen emails.');
          return;
        }

        const latestUid = results[results.length - 1];
        const f = imap.fetch(latestUid, { bodies: '' });

        f.on('message', function (msg, seqno) {
          console.log(`Processing message #${seqno}`);

          msg.on('body', function (stream, info) {
            let data = '';
            stream.on('data', function (chunk) {
              data += chunk.toString('utf8');
            });

            stream.on('end', function () {
              let body = { data: data };

              console.log('Data:', body);

            //   fetch(`${url}/mail`, {
            //     method: 'POST',
            //     headers: {
            //       'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify(body),
            //   })
            //     .then(response => response.json())
            //     .then(data => console.log('Email data sent:', data))
            //     .catch(error => console.error('Error sending email data:', error));
                axios.post(`${url}/mail`, body, {
                    headers: {
                    'Content-Type': 'application/json',
                    },
                })
                .then(response => {
                    console.log('Email data sent:', response.data);
                })
                .catch(error => {
                    console.error('Error sending email data:', error);
                });
            });
          });

          msg.once('attributes', function (attrs) {
            const { uid } = attrs;
            imap.addFlags(uid, '\\Seen', function (err) {
              if (err) {
                console.error('Error marking as read:', err);
              } else {
                console.log('Marked as read');
              }
            });
          });
        });

        f.once('error', function (err) {
          console.error('Fetch error:', err);
        });

        f.once('end', function () {
          console.log('Done fetching the latest unseen message.');
        });
      });
    });
  });
});

imap.once('error', function (err) {
  console.error('IMAP error:', err);
});

imap.once('end', function () {
  console.log('Connection ended');
});

imap.connect();

const MailParser = require("mailparser").MailParser;


function processMessage(msg, seqno) {
    console.log(`Processing message #${seqno}`);
    let subject = "";
    let body = { text: "", html: "", markdown: "" };
          
    var parser = new MailParser({ streamAttachments: true });
    parser.on("headers", function (headers) {
        subject = headers.get('subject'); // Extract subject from headers

    });

    parser.on('data', data => {
        if (data.type === 'text') {
            body.text = data.text; // Plain text version
            body.html = data.html || ""; // HTML version (if available)
            body.markdown = data.markdown || ""; // Markdown version (if available)
        }
    });
    let data = ""
    msg.on("body", function (stream) {
        stream.on("data", function (chunk) {
            data = data + chunk.toString("utf8");
            parser.write(chunk.toString("utf8"));
        });
        stream.on("end", (chunk) => {

        })
    });

    parser.on('attachment', async function (attachment, mail) {

    });

    msg.once("end", function () {
        
        parser.end();

        console.log("Data: ", data);

        //   Send email data to the server
        fetch(`${url}/mail`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              data: data,
                // subject: subject,
                // from: parsed.from.text,
                // to: parsed.to.text,
            }),
          }).then(response => response.json())
            .then(data => console.log('Email data sent:', data))
            .catch(error => console.log('Error sending email data:', error));



    });
}