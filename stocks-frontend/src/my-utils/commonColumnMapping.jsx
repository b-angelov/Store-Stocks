import React from "react";
import {DiAndroid, DiApple, DiWindows} from "react-icons/di";
import {MdCancel, MdCheckCircle, MdOutlineError} from "react-icons/md";
import Checkbox from "../components/checkbox";
import Progress from "../components/progress";
import {configure} from "@testing-library/react";
import {nanoid} from "nanoid";
import {nameMap} from "./nameRemapper";


function columnMapper(columnHelper, columnData, tableData, instanceId = null) {
    const iconApiURL = process.env.REACT_APP_ICON_API_URL || ""

    columnData = columnData.map((col) => {
        const columnTypes = {
            // NAME COLUMN
            name: () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">{col.Header}</p>
                ),
                cell: (info) => (
                    <p className="text-sm font-bold text-navy-700 dark:text-white">
                        {info.getValue()}
                    </p>
                ),
            }),
            tech: () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">{col.Header}</p>
                ),
                cell: (info) => (
                    <div className="flex items-center gap-2">
                        {info.getValue()?.map((item, key) => {
                            const instanceId = nanoid();
                            if (item === "apple") {
                                return (
                                    <div
                                        key={`${instanceId}-${col.accessor}-${key}`}
                                        className="text-[22px] text-gray-600 dark:text-white"
                                    >
                                        <DiApple/>
                                    </div>
                                );
                            } else if (item === "android") {
                                return (
                                    <div
                                        key={`${instanceId}-${col.accessor}-${key}`}
                                        className="text-[21px] text-gray-600 dark:text-white"
                                    >
                                        <DiAndroid/>
                                    </div>
                                );
                            } else if (item === "windows") {
                                return (
                                    <div
                                        key={`${instanceId}-${col.accessor}-${key}`}
                                        className="text-xl text-gray-600 dark:text-white"
                                    >
                                        <DiWindows/>
                                    </div>
                                );
                            } else return null;
                        })}
                    </div>
                ),
            }),


            // QUANTITY COLUMN
            quantity: () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">
                        {col.Header}
                    </p>
                ),
                cell: (info) => (
                    <p className="text-sm font-bold text-navy-700 dark:text-white">
                        {info.getValue()}
                    </p>
                ),
            }),
            date: () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">{col.Header}</p>
                ),
                cell: (info) => (
                    <p className="text-sm font-bold text-navy-700 dark:text-white">
                        {info.getValue()}
                    </p>
                ),
            }),
            progress: () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">
                        {col.Header}
                    </p>
                ),
                cell: (info) => (
                    <div className="flex items-center gap-3">
                        <p className="text-sm font-bold text-navy-700 dark:text-white">
                            {info.getValue()}%
                        </p>
                        <Progress key={nanoid()} width="w-[68px]" value={info.getValue()}/>
                    </div>
                ),
            }),


            // STATUS COLUMN
            "status": () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">
                        {col.Header}
                    </p>
                ),
                cell: (info) => (
                    <div className="flex items-center">
                        {info.getValue() === "Approved" ? (
                            <MdCheckCircle className="text-green-500 me-1 dark:text-green-300"/>
                        ) : info.getValue() === "Disable" ? (
                            <MdCancel className="text-red-500 me-1 dark:text-red-300"/>
                        ) : info.getValue() === "Error" ? (
                            <MdOutlineError className="text-amber-500 me-1 dark:text-amber-300"/>
                        ) : null}
                        <p className="text-sm font-bold text-navy-700 dark:text-white">
                            {info.getValue()}
                        </p>
                    </div>
                ),
            }),

            // CHECK COLUMN
            check: () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">{col.Header}</p>
                ),
                cell: (info) => (
                    <div className="flex items-center">
                        <Checkbox
                            defaultChecked={info.getValue()[1]}
                            colorScheme="brandScheme"
                            me="10px"
                        />
                        <p className="ml-3 text-sm font-bold text-navy-700 dark:text-white">
                            {info.getValue()[0]}
                        </p>
                    </div>
                ),
            }),


            // VENDOR COLUMN
            vendor: () => columnHelper.accessor(col.accessor, {
                id: col.accessor,
                header: () => (
                    <p className="text-sm font-bold text-gray-600 dark:text-white">{col.Header}</p>
                ),
                cell: (info) => {
                    const instanceId = nanoid();
                    let value = info.getValue()
                    if (typeof value === "string") value = [value]
                    return (<div className="flex items-center gap-2">
                        {value?.map((item, key) => {
                            return (
                                <figure key={`${instanceId}-${col.accessor}-${key}`}
                                        className={"flex item-center gap-3"}>
                                    <img alt={"brand logo"} className="h-8 w-8 flex"
                                         src={iconApiURL.replace("%searchable%", nameMap(item))}/>
                                    <span className={"capitalize font-bold"}>{item}</span>
                                </figure>

                            )
                        })}
                    </div>)
                }


            })
        }

        return columnTypes[col.type || "name"]()
    })
    return columnData
}

export default columnMapper