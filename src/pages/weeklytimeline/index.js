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

import { coaches, groups as g, items as i } from "./data/timelineData";
import { styleItem, styleGroup } from "utils/boxStyling";

// Timeline
import Timeline from "react-visjs-timeline";
import { useEffect, useState } from "react";

// material ui
import { Select, MenuItem, FormControl, OutlinedInput } from "@mui/material";

import './style.scss';

function WeeklyTimelineDashboard() {
  const [items, setItems] = useState(() => {
    return i.map(item => styleItem(item));
  });
  const [groups, setGroups] = useState(() => {
    return g.map(group => styleGroup(group));
  });
  // const [selectedGroups, setSelectedGroups] = useState(() => []);
  // const [all, setAll] = useState(() => false);
  const [startDate, setStartDate] = useState(() => moment("2023-11-14"));
  const [endDate, setEndDate] = useState(() => moment("2023-11-21"));

  const options = {
    showCurrentTime: false,
    showMajorLabels: false,
    stack: false,
    // start: new Date(2023, 10, 14, 12, 0, 0),
    // end: new Date(2023, 10, 14, 24, 0, 0),
    margin: {
      axis: 2.5,
      item: 5
    },
    min: new Date(2023, 10, 14, 0, 0, 0),
    max: new Date(2023, 10, 14, 24, 0, 0),
    editable: false,
    maxHeight: "70vh",
    orientation: "top",
    zoomMin: 3 * 60 * 60 * 1000,
    zoomMax: 24 * 60 * 60 * 1000
  };

  // useEffect(() => {
  //   setSelectedGroups(groups.filter(group => group.checked));
  // }, [groups]);

  // const handleSelect = (group_id) => {
  //   if (all) setAll(false);
  //   setGroups(groups.map(group => {
  //     if (group.id === group_id) group.checked = !group.checked;
  //     return group;
  //   }));
  // }

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pb={2}>
        <Grid container spacing={2}>
          <LocalizationProvider dateAdapter={AdapterMoment}>
            <Grid item>
              <DatePicker  value={startDate} onChange={setStartDate} classes={{ root: 'blueDatePicker' }} />
            </Grid>
            <Grid item>
              <DatePicker  value={endDate} onChange={setEndDate} classes={{ root: 'blueDatePicker' }} />
            </Grid>
          </LocalizationProvider>

          <Grid item>
            <FormControl>
              {/* <InputLabel id="mutiple-checkbox-label">Coach</InputLabel> */}
              <Select
                labelId="mutiple-checkbox-label"
                id="mutiple-checkbox"
                input={<OutlinedInput />}
                value={"Murad Hesham"}
                renderValue={(selected) => <div style={{padding: "12px 12px 12px 0px"}}>Murad Hesham</div>}
                displayEmpty
              >
                {coaches.map((coach) => (
                  <MenuItem key={coach.id} value={coach.content}>
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
      <Timeline className="timelinecustom" options={options} groups={groups} items={groups.length ? items : []} />
    </DashboardLayout>
  );
}

export default WeeklyTimelineDashboard;
