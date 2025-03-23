import * as React from 'react';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';

export default function ControlledSwitches({handleLableChange}) {
    const [state, setState] = React.useState({
        Graph: true,
      });
    
      const handleChange = (event) => {
        handleLableChange(event.target.checked)
        console.log(event.target.checked)
        console.log(event.target.name)
        setState({
          ...state,
          [event.target.name]: event.target.checked,
        });
      };

  return (
    <FormControlLabel
    control={
      <Switch checked={state.gilad} onChange={handleChange} name="graph" />
    }
    label="Graph"
  />
  );
}