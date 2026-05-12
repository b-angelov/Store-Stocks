import React from "react";
import columnMapper from "../../../../my-utils/commonColumnMapping";
import {createColumnHelper, flexRender, getCoreRowModel, getSortedRowModel, useReactTable} from "@tanstack/react-table";
import Card from "../../../../components/card";
import CardMenu from "../../../../components/card/CardMenu";
import {nanoid} from "nanoid";
import {MainSpinner} from "../../../../components/spinners/spinners";
import {MdChevronLeft, MdChevronRight} from "react-icons/md";

function CommonTable(props){
const { tableData, columnsData, columnParams, TableName, isLoading, isValidating,tablePagination,setPagination, paginationState, sorting, setSorting } = props;
  console.log(columnsData)
  // const [sorting, setSorting] = React.useState([]);
  let defaultData = tableData;
  const columns = columnMapper(columnHelper,columnsData,null,columnParams)
  console.log(tablePagination)
   // eslint-disable-next-line
  const [data, setData] = React.useState(() => [...defaultData]);
  const table = useReactTable({
    data,
    columns,
    pageCount: tablePagination?.total_pages,
    state: {
      sorting,
      pagination: paginationState,
    },
    onSortingChange: (updater)=>{
      setSorting(updater);
      setPagination((old)=>({...old,pageIndex:0}));
    },
    onPaginationChange: (updater) => {
    setPagination((old) => {
      const next = typeof updater === "function" ? updater(old) : updater;
      return next;
    });
  },
    manualPagination: true,
    manualSorting: true,
    // autoResetPageIndex: false,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    debugTable: true,
  });
  return (
    <Card extra={"w-full h-full sm:overflow-auto px-6"}>
      <header className="relative flex items-center justify-between pt-4">
        <div className="text-xl font-bold text-navy-700 dark:text-white">
          {TableName ?? ""}
        </div>

        <CardMenu />
      </header>

      <div className="mt-8 overflow-x-scroll xl:overflow-x-hidden">
        <table className="w-full">
          <thead>
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={nanoid()+headerGroup.id} className="!border-px !border-gray-400">
                {headerGroup.headers.map((header) => {
                  return (
                    <th
                      key={nanoid()+header.id}
                      colSpan={header.colSpan}
                      onClick={header.column.getToggleSortingHandler()}
                      className="cursor-pointer border-b-[1px] border-gray-200 pt-4 pb-2 pr-4 text-start"
                    >
                      <div className="items-center justify-between text-xs text-gray-200">
                        {flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                        {{
                          asc: "",
                          desc: "",
                        }[header.column.getIsSorted()] ?? null}
                      </div>
                    </th>
                  );
                })}
              </tr>
            ))}
          </thead>
          <tbody>
          {isValidating && (<tr><MainSpinner/></tr>)}
            {table
              .getRowModel()
              // .rows.slice(0, 5)
                .rows
              .map((row) => {
                return (
                  <tr key={nanoid()+row.id}>
                    {row.getVisibleCells().map((cell) => {
                      return (
                        <td
                          key={nanoid()+cell.id}
                          className="min-w-[150px] border-white/0 py-3  pr-4"
                        >
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </td>
                      );
                    })}
                  </tr>
                );
              })}
          </tbody>
        </table>
        <div className="flex items-center justify-between px-4 py-4">
  <div className="flex items-center gap-2">
    <button
      onClick={() => table.previousPage()}
      disabled={!table.getCanPreviousPage()}
      className="flex h-10 w-10 items-center justify-center rounded-full bg-brand-500 text-white disabled:bg-gray-200 dark:disabled:bg-navy-700"
    >
      <MdChevronLeft className="h-6 w-6" />
    </button>

    <span className="text-sm font-medium text-navy-700 dark:text-white">
      Страница {table.getState().pagination.pageIndex + 1} от {table.getPageCount()}
    </span>

    <button
      onClick={() => table.nextPage()}
      disabled={!table.getCanNextPage()}
      className="flex h-10 w-10 items-center justify-center rounded-full bg-brand-500 text-white disabled:bg-gray-200 dark:disabled:bg-navy-700"
    >
      <MdChevronRight className="h-6 w-6" />
    </button>
  </div>
</div>

      </div>
    </Card>
  );
}

export default CommonTable;
const columnHelper = createColumnHelper();