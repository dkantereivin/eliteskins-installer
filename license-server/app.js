const express = require('express');
const UIDGenerator = require('uid-generator');
const {Client} = require('pg');

// DB
const client = new Client({
    REDACTED
});

const app = express();

client.connect().then(() => console.log('connected to the db!'));
const uid = new UIDGenerator();

app.use(express.json());
app.use(express.urlencoded({extended: false}));

app.post('/license/', async (req, res) => {
    let key = await uid.generate();
    let qry = 'INSERT INTO licenses(key, uses, allowed_uses) VALUES ($1, 0, $2) RETURNING *;';
    await client.query(qry, [key, req.body.allowed_uses]);
    res.send({
        key,
        allowed_uses: req.body.allowed_uses
    });
});

app.post('/verify/', async (req, res) => {
    if (!req.body.key)
        return void res.status(200).send({success: false});
    let qry = 'SELECT * FROM licenses WHERE key=$1;';
    let data = (await client.query(qry, [req.body.key])).rows;
    if (data.length < 1) 
        return void res.status(200).send({success: false});
    
    if (!data[0].machine_id)
        data[0].machine_id = [];
    if (data[0].machine_id.includes(req.body.machine_id))
        data[0].uses -= 1;
    else
        data[0].machine_id.push(req.body.machine_id);
    if (data[0].uses >= data[0].allowed_uses)
        return void res.status(200).send({success: false});
    
    // proceed
    data[0].uses += 1;
    
    qry = 'UPDATE licenses SET uses=$1, machine_id=$2';
    client.query(qry, [data[0].uses, data[0].machine_id])
        .then(() => {
            res.status(200).send({success: true});
        });

});

app.get('/', (req, res) => {
    res.send(`<!DOCTYPE html><html><body>
    <form action="/license/" method="post">
        <input type="number" id="allowed_uses" name="allowed_uses">
        <input type="submit" value="Submit">
    </form>
    </body></html>`);
})

app.listen(process.env.PORT || 3000, () => {
    console.log('Working!')
})