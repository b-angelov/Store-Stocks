import {columnsModels} from "../variables/columnsData";
import {RenderTable} from "./RenderTable";
import {nameMap} from "../../../../my-utils/nameRemapper";

const columns = [
    {
    Header: "МАРКА",
    accessor: "brand",
    type: "vendor",
  },
  {
    Header:"МОДЕЛ",
    accessor: "model",
    type: "name",
  },
  {
    Header:"ТИП УСТРОЙСТВО",
    accessor: "device_type",
    type: "name"
  }
]

const mapFunction = (val)=>({
                ...val,
                brand:[val.brand_data.name||"samsung"],
                model:`${val.model} ${val.modification || ''}`,
                device_type:nameMap(val.device_type_data.device_type),
        })

export const Models = () =>{
    return (
        <RenderTable
            url="/models/?related=1"
            columns={columns}
            tableName = "Всички модели телефони"
            mapFunction = {mapFunction}
        />
    )
}