import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./style.sass";

interface LinkObj {
    id: number
    text: string
    to: string
    selected: boolean
}

interface LinkProps extends LinkObj {
    handleSelection: (id: number) => void
}

const NavLink: React.FC<LinkProps> = ({id, text, to, selected, handleSelection}) => {
    return (
        <Link
            className={`nav_link ${selected && "selected"}`}
            to={to}
            onClick={() => handleSelection(id)}
        >
            {text}
        </Link>
    );
};

const Sidebar: React.FC = () => {
    const [links, setLinks] = useState<Array<LinkObj>>([
        {id: 0, text: "Coach's schedule", to: "coach", selected: false},
        {id: 1, text: "Weekly schedule", to: "weekly", selected: false},
        {id: 2, text: "Location schedule", to: "location", selected: false}
    ]);

    useEffect(() => {
        const location: string = window.location.pathname.substring(1);
        
        setLinks(prev => [
            ...(prev.map(link => {
                if (link.to === location) link.selected = true;
                return link;
            }))
        ]);
    }, []);

    const handleSelection = (id: number) => {
        setLinks(prev => [
            ...(prev.map(link => {
                if (link.id === id) {
                    link.selected = true;
                } else link.selected = false

                return link;
            }))
        ]);
    }

    return (
        <div className="sidebar">
            <div className="sidebar__head">
                Company Name
            </div>
            <nav className="sidebar__nav">
                {links.map((link, index) => <NavLink handleSelection={handleSelection} key={index} {...link} />)}
            </nav>
        </div>
    );
};

export default Sidebar;
