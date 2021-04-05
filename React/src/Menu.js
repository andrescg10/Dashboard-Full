import { AppBar, Button, Fab, TextField, Toolbar } from "@material-ui/core";
import React, { useState } from "react";
import AddIcon from "@material-ui/icons/Add";
import Menu from "@material-ui/core/Menu";
import { makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import { TargetsMenu } from "./TargetsMenu";
import AccountBoxIcon from '@material-ui/icons/AccountBox';

const useStyles = makeStyles((theme) => ({
  text: {
    padding: theme.spacing(2, 2, 0),
  },
  paper: {
    paddingBottom: 50,
  },
  list: {
    marginBottom: theme.spacing(2),
  },
  appBar: {
    top: "auto",
    bottom: 0,
  },
  grow: {
    flexGrow: 1,
  },
  fabButton: {
    position: "absolute",
    zIndex: 1,
    top: -30,
    left: 0,
    right: 0,
    margin: "0 auto",
  },
}));

export const MenuBottom = () => {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  const [anchorTarget, setAnchorTarget] = useState(null);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClickTarget = (event) => {
    setAnchorTarget(event.currentTarget);
  };
  const handleCloseTarget = () => {
    setAnchorTarget(null);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const resetValues = () => {
    setUsername("");
    setPassword("");
    setProxy("");
    handleClose();
  };
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [proxy, setProxy] = useState("");
  const [dm_text, setDmText] = useState("");
  const [dm_link, setDmLink] = useState("");
  const [target, setTarget] = useState("");
  const [addTarget, setaddTarget] = useState("-");

  const handleAddTarget = async () => {
    await axios.post(`${process.env.REACT_APP_URL}/AddTargetList`, {
      target: addTarget,
    });
    setAnchorTarget(null);
  };

  const AddAccount = async () => {
    await axios
      .post(`${process.env.REACT_APP_URL}/AddAccount`, {
        username: username,
        password: password,
        proxy: proxy,
        dm_text: dm_text,
        dm_link: dm_link,
        target: target,
      })
      .then(resetValues());
  };
  return (
    <div>
      <AppBar
        position="fixed"
        style={{ backgroundColor: "black" }}
        className={classes.appBar}
      >
        <Toolbar>
          <Fab
            style={{ backgroundColor: "rgb(0, 227, 49)" }}
            className={classes.fabButton}
            onClick={handleClick}
          >
            <AddIcon />
          </Fab>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
            style={{ marginRight: "25%" }}
          >
            <div style={{ margin: "5%" }}>
              {" "}
              <TextField
                label="Username"
                onChange={(e) => {
                  setUsername(e.target.value);
                }}
              />
              <TextField
                label="Password"
                onChange={(e) => {
                  setPassword(e.target.value);
                }}
              />
              <TextField
                label="Proxy"
                onChange={(e) => {
                  setProxy(e.target.value);
                }}
              />
              <TextField
                label="Dm Text"
                onChange={(e) => {
                  setDmText(e.target.value);
                }}
              />
              <TextField
                label="DM Link"
                onChange={(e) => {
                  setDmLink(e.target.value);
                }}
              />
              <TextField
                label="Target"
                onChange={(e) => {
                  setTarget(e.target.value);
                }}
              />
              <div style={{ marginBottom: "8%" }} />
              <Button onClick={AddAccount} variant="contained">
                Add Account
              </Button>
            </div>
          </Menu>
          <Menu
            anchorEl={anchorTarget}
            open={Boolean(anchorTarget)}
            onClose={handleCloseTarget}
          >
            <TextField
              style={{ margin: "10%" }}
              label="Target Name use @ if it's a hashtag"
              onChange={(e) => {
                setaddTarget(e.target.value);
              }}
            >
              {" "}
            </TextField>
            <Button style={{ margin: "10%" }} onClick={handleAddTarget}>
              {" "}
              Add Target{" "}
            </Button>
          </Menu>
          <Fab onClick={handleClickTarget}>
            <AccountBoxIcon />
          </Fab>
          <div className={classes.grow} />
          <TargetsMenu />
        </Toolbar>
      </AppBar>
    </div>
  );
};
