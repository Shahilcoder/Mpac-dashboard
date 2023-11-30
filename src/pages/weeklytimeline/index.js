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

import { groups as g, items as i } from "./data/timelineData";
import { styleItem, styleGroup } from "utils/boxStyling";

// Timeline
import Timeline from "react-visjs-timeline";
import { useEffect, useState } from "react";

// material ui
import { Select, MenuItem, Checkbox, FormControl, OutlinedInput } from "@mui/material";

import './style.scss';

function WeeklyTimelineDashboard() {
  const [items, setItems] = useState(() => {
    return i.map(item => styleItem(item));
  });
  const [groups, setGroups] = useState(() => {
    return g.map(group => styleGroup(group));
  });
  const [selectedGroups, setSelectedGroups] = useState(() => []);
  const [all, setAll] = useState(() => false);
  const [selectedDate, setSelectedDate] = useState(() => moment("2023-11-14"));

  const options = {
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

  useEffect(() => {
    setSelectedGroups(groups.filter(group => group.checked));
  }, [groups]);

  const handleSelect = (group_id) => {
    if (all) setAll(false);
    setGroups(groups.map(group => {
      if (group.id === group_id) group.checked = !group.checked;
      return group;
    }));
  }

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pb={2}>
        <Grid container spacing={2}>
          <Grid item>
            <LocalizationProvider dateAdapter={AdapterMoment}>
              <DatePicker  value={selectedDate} onChange={setSelectedDate} classes={{ root: 'blueDatePicker' }} />
            </LocalizationProvider>
          </Grid>

          <Grid item>
            <FormControl>
              {/* <InputLabel id="mutiple-checkbox-label">Coach</InputLabel> */}
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
                    setGroups(groups.map(group => { group.checked = !all; return group; }));
                    setAll(!all);
                  }}
                >
                  <Checkbox checked={all} />
                  Select All
                </MenuItem>
                {groups.map((group) => (
                  <MenuItem key={group.id} value={group.content} onClick={() => handleSelect(group.id)}>
                    <Checkbox checked={group.checked} />
                    {group.content}
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
            <div className="legend_uae"></div> Program in UAE
          </div>
        </div>
      </MDBox>
      <Timeline className="timelinecustom" options={options} groups={selectedGroups} items={selectedGroups.length ? items : []} />
    </DashboardLayout>
  );
}

export default WeeklyTimelineDashboard;
