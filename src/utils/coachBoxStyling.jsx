import moment from "moment";

export const styleItem = (item) => {
    if (["office", "buffer", "lunch"].includes(item._type)) {
        return {
            ...item,
            className: `timeline_item_${item._type}`,
            content: item._type[0].toUpperCase() + item._type.substr(1)
        };
    }
    else if (["dubai", "sharjah", "abudhabi"].includes(item._type)) {
        return {
            ...item,
            className: `timeline_item_${item._type}`,
            content: `<div>
                <div>
                    <div>${item.data.school}</div>
                    <div>${item.data.court}</div>
                </div>

                <div>
                    <div>${item.data.program}</div>
                    <div>level: ${item.data.level}</div>
                    <div>age group: ${item.data.age_group}</div>
                    <div>${moment(item.start).format('hh:mm a')} - ${moment(item.end).format('hh:mm a')}</div>
                </div>
            </div>`
        }
    }
    else {
        return {
            ...item,
            className: "timeline_item",
            content: `<div>
                <div>
                    <div>${item.data.school}</div>
                    <div>${item.data.court}</div>
                </div>

                <div>
                    <div>${item.data.program}</div>
                    <div>level: ${item.data.level}</div>
                    <div>age group: ${item.data.age_group}</div>
                    <div>${moment(item.start).format('hh:mm a')} - ${moment(item.end).format('hh:mm a')}</div>
                </div>
            </div>`
        }
    }
};

export const styleGroup = (group) => {
    return {
        ...group,
        checked: false
    }
};
