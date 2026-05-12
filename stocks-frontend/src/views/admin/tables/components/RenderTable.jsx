import useSWR from "swr";
import {fetcher} from "../../../../API/API";
import {useMemo, useState} from "react";
import {nameMap} from "../../../../my-utils/nameRemapper";
import CommonTable from "./CommonTable";
import {columnsModels} from "../variables/columnsData";
import {FadeLoader} from "react-spinners";
import {MainSpinner} from "../../../../components/spinners/spinners";

export const RenderTable = ({url, columns, tableName,mapFunction, preProcessDataFn, columnParams}) => {
  preProcessDataFn = preProcessDataFn ?? (val=>val);
  const [pagination, setPagination] = useState({
        pageIndex: 0,
        pageSize: 15,
      })
    const [sorting, setSorting] = useState([{
        id: "id",
        desc: false
    }])
    const sortParams = "&" + sorting.map((st)=>{
        return `sort=${st.desc?"-":""}${st.id}`
    }).join("&")
    const {data:ModelsData, error, isLoading, isValidating} = useSWR(`${url}&page=${pagination?.pageIndex + 1}&page_size=${pagination?.pageSize ?? 10}${sortParams}`,fetcher,
        {
    keepPreviousData: false,
    revalidateOnFocus: false,
    dedupingInterval: 0,
  })
    const processedData = useMemo((data)=>{
        if (!ModelsData) return {}
        console.log(ModelsData.items)
        return {data: preProcessDataFn(ModelsData?.items?.map(mapFunction)), pagination:ModelsData?.pagination}
    },[ModelsData])
    let component;
    if(error) component =(<div className={"error-decor"}>Something went wrong with table data loading!{error.code}</div>);
  if(ModelsData) component = (

      <div className="mt-1 grid h-full grid-cols-1 gap-5 md:grid-cols-1">
          {ModelsData && (<><CommonTable
          columnsData={columns}
          tableData={processedData.data}
          tablePagination={processedData.pagination}
          paginationState = {pagination}
          TableName = {tableName}
          isValidating = {isValidating}
          isloading = {isLoading}
          setPagination = {setPagination}
          sorting={sorting}
          setSorting = {setSorting}
          columnParams={columnParams}
          key={`${url}&page=${pagination?.pageIndex + 1}&page_size=${pagination?.pageSize ?? 10}${sortParams}`}
        /></>)}
      </div>)
    return component
}