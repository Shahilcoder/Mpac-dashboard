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

import { coaches, locations as g, programs as p } from "./data/timelineData";
import { styleItem, styleGroup } from "utils/locationBoxStyle";

// Timeline
import Timeline from "react-visjs-timeline";
import { useState } from "react";

// material ui
import { Select, MenuItem, FormControl, OutlinedInput } from "@mui/material";
import { Modal, Box, Typography } from "@mui/material";

import './style.scss';

function LocationTimelineDashboard() {
  const [programs] = useState(() => {
    return p.map(program => styleItem(program));
  });
  const [groups] = useState(() => {
    return g.map(group => styleGroup(group));
  });

  const [selectedDate, setSelectedDate] = useState(() => moment("2023-11-14"));
  const [open, setOpen] = useState(() => false);

  const [selectedCoach, setSelectedCoach] = useState(() => "Select Coach");

  const options = {
    showCurrentTime: false,
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
    zoomMin: 2.2 * 60 * 60 * 1000,
    zoomMax: 24 * 60 * 60 * 1000
  };

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <div className="locationtimeline">
        <MDBox pb={2}>
          <Modal
            open={open}
            onClose={() => setOpen(false)}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
          >
            <Box sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: 400,
              bgcolor: 'background.paper',
              // border: '2px solid #000',
              boxShadow: 24,
              p: 4,
            }}>
              <Typography id="modal-modal-title" variant="h6" component="h2">
                Select Coach
              </Typography>
              <div id="modal-modal-description" sx={{ mt: 2 }}>
                <FormControl>
                  <Select
                    labelId="mutiple-checkbox-label"
                    id="mutiple-checkbox"
                    input={<OutlinedInput />}
                    value={selectedCoach}
                    renderValue={(selected) => <div style={{padding: "12px 12px 12px 0px"}}>{selected}</div>}
                    onChange={(e) => setSelectedCoach(e.target.value)}
                  >
                    {coaches.map((coach) => (
                      <MenuItem key={coach.id} value={coach.content}>
                        {coach.content}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </div>
            </Box>
          </Modal>
          <Grid container spacing={2}>
            <Grid item>
              <LocalizationProvider dateAdapter={AdapterMoment}>
                <DatePicker  value={selectedDate} onChange={setSelectedDate} classes={{ root: 'blueDatePicker' }} />
              </LocalizationProvider>
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
        <Timeline options={options} groups={groups} items={groups.length ? programs : []} selectHandler={(props) => setOpen(true)} />
      </div>
    </DashboardLayout>
  );
}

export default LocationTimelineDashboard;
