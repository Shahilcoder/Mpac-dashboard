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

import { coaches, weeks as w, programs as p } from "./data/timelineData";
import { styleItem, styleGroup } from "utils/weeklyBoxStyling";

// Timeline
import Timeline from "react-visjs-timeline";
import { useState } from "react";

// material ui
import { Select, MenuItem, FormControl, OutlinedInput } from "@mui/material";

import './style.scss';

function WeeklyTimelineDashboard() {
  const [programs] = useState(() => {
    return p.map(program => styleItem(program));
  });
  const [weeks] = useState(() => {
    return w.map(week => styleGroup(week));
  });

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
    format: {
      minorLabels: {
        hour: "hh:mm a",
        minute: "hh:mm a"
      }
    },
    editable: false,
    maxHeight: "70vh",
    orientation: "top",
    zoomMin: 2.3 * 60 * 60 * 1000,
    zoomMax: 24 * 60 * 60 * 1000
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <div className="weeklytimeline">
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
        <Timeline options={options} groups={weeks} items={weeks.length ? programs : []} />
      </div>
    </DashboardLayout>
  );
}

export default WeeklyTimelineDashboard;
