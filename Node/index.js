const express = require("express");
const app = express();
const database = require("./Database/Pool").mongoConnect;
const getDb = require("./Database/Pool").getDb;
const cors = require("cors");
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.get("/ListAccounts", async (req, res) => {
  const db = getDb();
  await db
    .collection("AccountsManage")
    .find({})
    .toArray()
    .then((r) => {
      res.send(r);
    }).catch((e) => res.send(e));
});

app.post("/AddAccount", async (req, res) => {
  const db = getDb();
  await db
    .collection("AccountsManage")
    .insertOne(req.body)
    .then((r) => res.send(r));
    await db
    .collection("pending")
    .insertOne(req.body)
    .then((r) => res.send(r))
    .catch((e) => {
      res.send(e);
    });
});

app.post("/AddTarget", async (req, res) => {
  const db = getDb();
  const { target } = req.body;
  target[0] === "@"
    ? (collectionFinal = "Hashtags")
    : (collectionFinal = "AccountsFollowers");
  await db
    .collection(collectionFinal)
    .insertOne(req.body)
    .then((r) => {
      res.send("Added");
    });
});

app.post("/AddTargetList", async (req, res) => {
  const db = getDb();
  await db
    .collection("AccountsTarget")
    .insertOne(req.body)
    .then((r) => {
      res.send("Added");
    });
});

app.get("/Targets", async (req, res) => {
  const db = getDb();
  await db
    .collection("AccountsTarget")
    .find({})
    .toArray()
    .then((r) => {
      res.send(r);
    });
});

app.get("/ListHashtags", async (req, res) => {
  const db = getDb();
  await db
    .collection("Hashtags")
    .find({})
    .toArray()
    .then((r) => res.send(r));
});

app.get("/ListTargetFollowers", async (req, res) => {
  const db = getDb();
  await db
    .collection("AccountsFollowers")
    .find({})
    .toArray()
    .then((r) => {
      res.send(r);
    });
});

app.post("/AddTargetFollowers", async (req, res) => {
  const db = getDb();

  await db
    .collection("AccountsFollowers")
    .insertOne(req.body)
    .then((r) => {
      res.send("Added Target");
    })
    .catch((e) => {
      res.send(e);
    });
});

app.post("/DeleteTargetFollowers", async (req, res) => {
  const db = getDb();
  const { targetName } = req.body;
  await db
    .collection("AccountsFollowers")
    .deleteOne({ target: targetName })
    .then((r) => {
      res.send(r);
    })
    .catch((e) => {
      res.send(e);
    });
});

app.post("/DeleteHashtag", async (req, res) => {
  const db = getDb();
  const { targetName } = req.body;
  await db
    .collection("Hashtags")
    .deleteOne({ target: targetName })
    .then((r) => {
      res.send(r);
    })
    .catch((e) => {
      res.send(e);
    });
});

app.post("/DeleteAccount", async (req, res) => {
  const db = getDb();
  const { username } = req.body;
  await db
    .collection("AccountsManage")
    .deleteOne({ username: username })
    .then((r) => {
      res.send(r);
    })
    .catch((e) => {
      res.send(e);
    });
  await db
    .collection("pending")
    .deleteOne({ username: username })
    .then((r) => res.send(r))
    .catch((e) => res.send(e));
});

app.post("/UpdateTarget", async (req, res) => {
  const db = getDb();
  const { username, target } = req.body;
  await db
    .collection("AccountsManage")
    .updateOne({ username: username }, { $set: { target: target } })
    .then((r) => {
      res.send(r);
    })
    .catch((e) => {
      res.send(e);
    });
});

app.post("/UpdateDM", async (req, res) => {
  const db = getDb();
  const { username, dm_text, dm_link } = req.body;
  console.log(username);
  console.log(dm_text);
  console.log(dm_link);
  await db
    .collection("AccountsManage")
    .updateOne(
      { username: username },
      { $set: { dm_text: dm_text, dm_link: dm_link } }
    )
    .then((r) => {
      res.send(r);
    })
    .catch((e) => {
      res.send(e);
    });
});

app.post("/UpdateCreds", async (req, res) => {
  const db = getDb();
  const { username, creds } = req.body;
  console.log(`${username} got creds`);
  await db
    .collection("AccountsManage")
    .updateOne({ username: username }, { $set: { creds: creds } })
    .then((r) => {
      res.send(r);
    })
    .catch((e) => {
      res.send(e);
    });
});

app.get("/ToMakeCreds", async (req, res) => {
  const db = getDb();
  await db
    .collection("pending")
    .find({})
    .toArray()
    .then((r) => res.send(r))
    .catch((e) => res.send(e));
});


app.get("/accountsCreds", async (req, res) => {
  const db = getDb();
  await db
    .collection("pending")
    .find({})
    .toArray()
    .then((r) => res.send(r))
    .catch((e) => res.send(e));
});

app.post("/DeleteCred", async (req, res) => {
  const { username } = req.body;
  const db = getDb();
  await db
    .collection("pending")
    .deleteOne({ username: username })
    .then((r) => {
      res.send(r);
    })
    .catch((e) => {
      res.send(e);
    });
});

app.get("/", (req, res) => {
  res.send("Hello");
});

database(() => {
  app.listen(port);
});
