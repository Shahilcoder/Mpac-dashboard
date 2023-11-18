import React from "react";
import avatar from "/src/assets/male_avatar.jpg";
import "./style.sass";

const Header: React.FC = () => {
    return (
        <div className="header">
            <div className="header__avatar">
                <img src={avatar} alt="Avatar" />
            </div>
        </div>
    );
};

export default Header;
