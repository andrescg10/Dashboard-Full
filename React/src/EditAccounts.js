import { Button, TextField } from "@material-ui/core";
import React, { useState } from "react";
import EditIcon from "@material-ui/icons/Edit";
import Menu from "@material-ui/core/Menu";
import axios from "axios";
export const EditAccounts = ({ dm_text, dm_link, username }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const [dmText, setDmText] = useState()
  const [dmLink, setDmLink] = useState()
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleCall = async () => {
      await axios.post(`${process.env.REACT_APP_URL}/UpdateDM`, {username, dm_text: dmText, dm_link: dmLink})
  }
  return (
    <>
      <Button onClick={handleClick}>
        <EditIcon />
      </Button>
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        <p>{`Your actual dm text is ${dm_text}`}</p>
        <p>{`Your actual dm link is ${dm_link}`}</p>
        <TextField
          onChange={(e) => {
            setDmText(e.target.value);
          }}
          label="New Dm Text"
        ></TextField>
        <TextField
          onChange={(e) => {
            setDmLink(e.target.value);
          }}
          label="New Dm Link"
        ></TextField>
        <Button onClick={handleCall} variant="contained">Submit Your New DM Info</Button>
      </Menu>
    </>
  );
};
