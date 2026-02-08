import React, { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import AuthLoaderButton from "../../components/AuthLoaderButton";
import { Formik, Form, ErrorMessage, Field } from "formik";
import * as yup from "yup";
import { axiosClient } from "../../utils/axiosClient";
import toast from "react-hot-toast";
import { Link } from "react-router-dom";

const LoginPage = () => {
  const [ishide, setHide] = useState(true);
  const [isloading, setloading] = useState(false);
  const validationSchema = yup.object({
    email: yup
      .string()
      .required("Email is required")
      .email("Invalid email format")
      .matches(/.+\..+/, "Email domain must contain a dot"),

    password: yup
      .string()
      .min(6, "Password must be at least 6 characters")
      .required("Password is required"),
  });

  const onSubmitHandler = async (values, helpers) => {
    try {
      setloading(true);

      const response = await axiosClient.post("/auth/login", values);
      // console.log(values);
      const data = response.data;
      console.log(data);
      toast.success("Login successfully!");
      localStorage.setItem("token",data.token)

      helpers.resetForm();
    } catch (error) {
      let message = "Something went wrong";

      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          message = detail
            .map((err) => `${err.loc[err.loc.length - 1]}: ${err.msg}`)
            .join(", ");
        } else if (typeof detail === "string") {
          message = detail;
        }
      }

      toast.error(message);
    } finally {
      setloading(false);
    }
  };

  const initialValue = {
    email: "",
    password: "",
  };

  return (
    <div>
      <div className="min-h-[80vh] flex justify-center items-center">
        <Formik
          validationSchema={validationSchema}
          initialValues={initialValue}
          onSubmit={onSubmitHandler}
        >
          <Form className="w-[96%] mx-auto py-10 px-8 lg:w-1/2 bg-gray-200 border border-gray-800 rounded-4xl shadow">
            <div className="mb-3">
              <label htmlFor="email" className=" text-gray-700 font-bold mb-2 ">
                Email<span className="text-red-500">*</span>
              </label>
              <Field
                autoComplete="off"
                name="email"
                id="email"
                type="email"
                className="w-full py-3 px-4  border rounded-2xl outline-none transition-all duration-300
             border-gray-400 focus:ring-1"
                placeholder="Enter your Email"
              />
              <ErrorMessage
                name="email"
                className="text-red-500"
                component={"p"}
              />
            </div>
            <div className="mb-3">
              <label
                htmlFor="password"
                className=" text-gray-700 font-bold mb-2 "
              >
                Password <span className="text-red-500">*</span>
              </label>
              <div
                className="rounded-2xl outline transition-all duration-300
             border-gray-200 focus:ring-1 flex justify-between align-center "
              >
                <Field
                  autoComplete="off"
                  name="password"
                  id="password"
                  type={ishide ? "password" : "text"}
                  className="w-full py-3 px-4  border border-gray-200 "
                  placeholder="Enter your password"
                />
                <button
                  onClick={() => setHide(!ishide)}
                  type="button"
                  className="text-2xl"
                >
                  {ishide ? <FaEye /> : <FaEyeSlash />}
                </button>
              </div>
              <ErrorMessage
                name="password"
                className="text-red-500"
                component={"p"}
              />
            </div>
            <div className="mb-3">
              <AuthLoaderButton isloading={isloading} text={"Login"} />
            </div>
            <div className="mb-3">
              <p className="text-end">
                Don't have an account? <Link to={"/register"}>Register</Link>
              </p>
            </div>
          </Form>
        </Formik>
      </div>
    </div>
  );
};

export default LoginPage;
