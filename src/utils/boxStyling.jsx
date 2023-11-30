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
