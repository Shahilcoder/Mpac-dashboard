export const styleItem = (item) => {
    if (item._type === "office") {
        return {
            ...item,
            className: "timeline_item_office",
            content: "Office"
        };
    }
    else if (item._type === "buffer") {
        return {
            ...item,
            className: "timeline_item_buffer",
            content: "Buffer"
        }
    }
    else if (item._type === "lunch") {
        return {
            ...item,
            className: "timeline_item_lunch",
            content: "Lunch"
        };
    }
    else if (item._type === "uae") {
        return {
            ...item,
            className: "timeline_item_uae",
            content: `<div>
                <div>
                    <div>${item.data.school}</div>
                    <div>${item.data.court}</div>
                </div>

                <div>
                    <div>${item.data.program}</div>
                    <div>${item.data.class_type}</div>
                    <div>${item.data.level}</div>
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
                    <div>${item.data.class_type}</div>
                    <div>${item.data.level}</div>
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
