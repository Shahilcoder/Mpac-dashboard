import React from "react";
import "./style.sass";

const Title: React.FC<{ text: string }> = ({ text }) => {
    return (
        <div className="title">
            {text}
        </div>
    );
};

export default Title;
