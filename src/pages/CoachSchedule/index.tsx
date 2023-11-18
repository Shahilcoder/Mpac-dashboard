import React from "react";
import { Chart } from "react-google-charts";
import { data } from "./data";
// import Title from "../../components/Title";
import "./style.sass";

const CoachSchedule: React.FC = () => {

    return (
        <div>
            {/* <Title text="Coach's Schedule" /> */}
            <div className="date_time">
                14 November 2023
            </div>
            <Chart
                chartType="Timeline"
                data={data}
                options={{
                    timeline: { 
                        colorByRowLabel: true,
                        rowLabelStyle: {
                            color: "#000000",
                            fontSize: 16
                        }
                    },
                    hAxis: {
                        1: {
                            textStyle: {
                                color: '#4caf50', // Set the color of the axis labels
                            }
                        }
                    },
                    backgroundColor: "#ffffff",
                    alternatingRowStyle: false
                }}
                width="100%"
                height="80vh"
            />
        </div>
    );
};

export default CoachSchedule;
