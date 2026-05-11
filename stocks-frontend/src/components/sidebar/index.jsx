/* eslint-disable */

import { HiX } from "react-icons/hi";
import Links from "./components/Links";
import logo from "assets/img/layout/smartcomp-logo.png"

import SidebarCard from "components/sidebar/componentsrtl/SidebarCard";
import routes from "routes.js";

const Sidebar = ({ open, onClose }) => {
  return (
    <div
      className={`sm:none duration-175 linear fixed !z-50 flex min-h-full flex-col bg-white pb-10 shadow-2xl shadow-white/5 transition-all dark:!bg-navy-800 dark:text-white md:!z-50 lg:!z-50 xl:!z-0 ${
        open ? "translate-x-0" : "-translate-x-96"
      }`}
    >
      <span
        className="absolute top-4 right-4 block cursor-pointer xl:hidden"
        onClick={onClose}
      >
        <HiX />
      </span>

      <div className={`mx-[56px] mt-[50px] pb-10 flex items-center`}>
        <div className="mt-1 ml-1 h-2.5 pb-1.5 font-poppins text-[26px] font-bold uppercase text-navy-700 dark:text-white">
          <span className={"pb-12 relative text-shadow-lg"} style={{ textShadow: "4px 1px 4px rgba(0,0,0,0.4)" }}>умен<span class="font-medium"> магазин</span></span>
          <img className={"mt-1 ml-1 mb-1 h-14 w-3/4 shadow-xl pb-1 relative content-center items-center left-5"} src={logo} alt={"Logo"} />
        </div>
      </div>
      <div class="mt-[58px] mb-7 h-px bg-gray-300 dark:bg-white/30" />
      {/* Nav item */}

      <ul className="mb-auto pt-1">
        <Links routes={routes} />
      </ul>

      {/* Free Horizon Card */}
      <div className="flex justify-center">
        {/*<SidebarCard />*/}
      </div>

      {/* Nav item end */}
    </div>
  );
};

export default Sidebar;
