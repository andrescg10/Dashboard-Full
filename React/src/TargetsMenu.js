import React, { useEffect, useState } from "react";
import NativeSelect from "@material-ui/core/NativeSelect";
import { Button, TextField, Fab } from "@material-ui/core";
import axios from 'axios'
import Menu from "@material-ui/core/Menu";

import SearchIcon from '@material-ui/icons/Search';

export const TargetsMenu = () => {
  const [targets, setTargets] = useState([]);
  const [selectedT, setT] = useState("");
  const [amount, setAmount] = useState()
  const [anchorEl, setAnchorEl] = useState(null)
  const totalAmount = parseInt(amount)
  const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };
  const HandleChange = (e) => {
    setT(e.target.value);
  };
  const fetchTargets = async () => {
    const TargetList = await axios.get(`${process.env.REACT_APP_URL}/Targets`);
    setTargets(TargetList.data);
  };
  useEffect(() => {
    fetchTargets();
  }, []);

  const handleSubmit = async () => { await axios.post(`${process.env.REACT_APP_URL}/AddTarget`, {
      target: selectedT,
      amount: totalAmount
  }) }
  const TargetsList = targets.map(({ _id, target }) => (
    <option key={_id} value={target}>
      {target}
    </option>
  ));


  return (
    <>    <Menu
    anchorEl={anchorEl}
    open={Boolean(anchorEl)}
    onClose={handleClose}
  >
      <NativeSelect style={{margin: '10%'}} onChange={HandleChange}>{TargetsList}</NativeSelect>
      <TextField style={{margin: '10%'}} onChange={(e) => setAmount(e.target.value)} label="Amount scrape (Numbers)"> </TextField>
      <Button onClick={handleSubmit}style={{margin: "10%"}}> Scrape </Button>
      </Menu>
      <Fab onClick={handleClick}>
            <SearchIcon />
          </Fab>
    </>
  );
};
