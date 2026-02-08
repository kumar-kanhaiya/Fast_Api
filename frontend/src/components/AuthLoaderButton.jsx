import React, { useState } from "react";
import { CgSpinner } from "react-icons/cg";
import { FaArrowRight } from "react-icons/fa";

const AuthLoaderButton = ({ isloading = false, text, className }) => {
  return (
    <div>
      <button
        disabled={isloading}
        className={
          "flex justify-center align-center w-full py-3 rounded bg-blue-600 disabled:bg-blue-900 cursor-pointer border-none outline-none disabled:cursor-no-drop" +
          className
        }
      >
        <span>{text}</span>
        {isloading ? (
          <CgSpinner className="animate-spin text-xl text-white" />
        ) : (
          <FaArrowRight />
        )}
      </button>
    </div>
  );
};

export default AuthLoaderButton;
