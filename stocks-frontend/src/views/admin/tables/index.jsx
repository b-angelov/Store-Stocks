import CheckTable from "./components/CheckTable";

import {
  columnsDataDevelopment,
  columnsDataCheck,
  columnsDataColumns,
  columnsDataComplex,
    columnsPhones,
} from "./variables/columnsData";
import tableDataDevelopment from "./variables/tableDataDevelopment.json";
import tableDataCheck from "./variables/tableDataCheck.json";
import tableDataColumns from "./variables/tableDataColumns.json";
import tableDataComplex from "./variables/tableDataComplex.json";
import DevelopmentTable from "./components/DevelopmentTable";
import ColumnsTable from "./components/ColumnsTable";
import ComplexTable from "./components/ComplexTable";
import CommonTable from "./components/CommonTable";
import useSWR from "swr";
import {fetcher} from "../../../API/API";
import {useMemo} from "react";
import {nameMap} from "../../../my-utils/nameRemapper";
import {Phones} from "./components/Phones";
import {Models} from "./components/Models";

const Tables = () => {
  return (
    <div>
      <div className="mt-1 grid h-full grid-cols-1 gap-5 md:grid-cols-1">
          <Phones/>
          <Models/>
        <CommonTable
          columnsData={columnsDataDevelopment}
          tableData={tableDataDevelopment}
        />
        <CommonTable columnsData={columnsDataCheck} tableData={tableDataCheck} />
      </div>

      <div className="mt-8 grid h-full grid-cols-1 gap-5 md:grid-cols-1">
        <CommonTable
          columnsData={columnsDataColumns}
          tableData={tableDataColumns}
        />

        <CommonTable
          columnsData={columnsDataComplex}
          tableData={tableDataComplex}
        />
      </div>
    </div>
  );
};

export default Tables;
