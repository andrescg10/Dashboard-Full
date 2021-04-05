import React from 'react'
import DeleteIcon from "@material-ui/icons/Delete"
import { Button } from '@material-ui/core'
import axios from 'axios'

export const DeleteButton = (username) => {
    const handleDelete = async() => {
        await axios.post(`${process.env.REACT_APP_URL}/DeleteAccount`, username)
    }
    return (
        <>
        <Button onClick={handleDelete}>
          <DeleteIcon />
          </Button>  
        </>
    )
}
