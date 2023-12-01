import Grid from "@mui/material/Grid";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";

// Material Dashboard 2 React example components
import DashboardLayout from "components/LayoutContainers/DashboardLayout";
import DashboardNavbar from "components/Navbars/DashboardNavbar";

// Date
import moment from "moment";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";

import { coaches as c, programs as p } from "./data/timelineData";
import { styleItem, styleGroup } from "utils/coachBoxStyling";

// Timeline
import Timeline from "react-visjs-timeline";
import { useEffect, useState } from "react";

// material ui
import { Select, MenuItem, Checkbox, FormControl, OutlinedInput } from "@mui/material";

import './style.scss';

function CoachTimelineDashboard() {
  const [programs] = useState(() => {
    return p.map(program => styleItem(program));
  });
  const [coaches, setCoaches] = useState(() => {
    return c.map(coach => styleGroup(coach));
  });

  const [selectedCoaches, setSelectedCoaches] = useState(() => []);

  const [all, setAll] = useState(() => false);

  const [selectedDate, setSelectedDate] = useState(() => moment("2023-11-14"));

  const options = {
    showCurrentTime: false,
    stack: false,
    start: new Date(2023, 10, 14, 10, 0, 0),
    // end: new Date(2023, 10, 14, 24, 0, 0),
    margin: {
      axis: 2.5,
      item: 5
    },
    min: new Date(2023, 10, 14, 0, 0, 0),
    max: new Date(2023, 10, 14, 24, 0, 0),
    format: {
      minorLabels: {
        hour: "hh:mm a",
        minute: "hh:mm a"
      }
    },
    editable: false,
    maxHeight: "70vh",
    orientation: "top",
    zoomMin: 2.2 * 60 * 60 * 1000,
    zoomMax: 24 * 60 * 60 * 1000
  };

  useEffect(() => {
    setSelectedCoaches(coaches.filter(coach => coach.checked));
  }, [coaches]);

  const handleSelect = (coach_id) => {
    if (all) setAll(false);
    setCoaches(coaches.map(coach => {
      if (coach.id === coach_id) coach.checked = !coach.checked;
      return coach;
    }));
  }

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <div className="coachtimeline">
        <MDBox pb={2}>
          <Grid container spacing={2}>
            <Grid item>
              <LocalizationProvider dateAdapter={AdapterMoment}>
                <DatePicker  value={selectedDate} onChange={setSelectedDate} classes={{ root: 'blueDatePicker' }} />
              </LocalizationProvider>
            </Grid>

            <Grid item>
              <FormControl>
                <Select
                  labelId="mutiple-checkbox-label"
                  id="mutiple-checkbox"
                  input={<OutlinedInput />}
                  value={[]}
                  renderValue={(selected) => <em style={{padding: "12px 12px 12px 0px"}}>Select Coaches</em>}
                  multiple
                  displayEmpty
                >
                  <MenuItem onClick={() => {
                      setCoaches(coaches.map(coach => { coach.checked = !all; return coach; }));
                      setAll(!all);
                    }}
                  >
                    <Checkbox checked={all} />
                    Select All
                  </MenuItem>
                  {coaches.map(coach => (
                    <MenuItem key={coach.id} value={coach.content} onClick={() => handleSelect(coach.id)}>
                      <Checkbox checked={coach.checked} />
                      {coach.content}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </MDBox>
        <MDBox pb={2}>
          <div className="legend">
            <div>
              <div className="legend_normal"></div> Program
            </div>
            <div>
              <div className="legend_buffer"></div> Buffer
            </div>
            <div>
              <div className="legend_office"></div> Office
            </div>
            <div>
              <div className="legend_lunch"></div> Lunch
            </div>
            <div>
              <div className="legend_dubai"></div> Program in Dubai
            </div>
            <div>
              <div className="legend_sharjah"></div> Program in Sharjah
            </div>
            <div>
              <div className="legend_abudhabi"></div> Program in Abu Dhabi
            </div>
          </div>
        </MDBox>
        <Timeline options={options} groups={selectedCoaches.length ? selectedCoaches : [{id: 0, content: ""}]} items={selectedCoaches.length ? programs : []} />
      </div>
    </DashboardLayout>
  );
}

export default CoachTimelineDashboard;
