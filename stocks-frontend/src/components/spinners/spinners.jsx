import {FadeLoader} from "react-spinners";
import Card from "../card";

export const MainSpinner = (props) => {
    return (

        <div
            className="absolute inset-0 z-50 flex items-center justify-center bg-white/20 backdrop-blur-[2px] dark:bg-navy-900/20">
            <FadeLoader {...props} />
            {/*<div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center">*/}
            {/*    <div*/}
            {/*        className="h-12 w-12 animate-spin rounded-full border-4 border-solid border-brand-500 border-t-transparent shadow-xl"></div>*/}
            {/*    <p className="mt-4 font-bold text-brand-500 dark:text-white">Зареждане...</p>*/}
            {/*</div>*/}
        </div>


    )
}