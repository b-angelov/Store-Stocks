import {columnsAccessories, columnsPhones} from "../variables/columnsData";
import {RenderTable} from "./RenderTable";
import {nameMap} from "../../../../my-utils/nameRemapper";

const columns = [
  {
    Header: "Вид Аксесоар",
    accessor: "accessory_type",
    type: "name"

  },
  {
    Header: "ЗА",
    accessor: "for_device_type",
    type:"name"
  },
  {
    Header: "МАРКА",
    accessor: "for_device_brand",
    type: "vendor"
  },
  {
    Header: "МОДЕЛ",
    accessor: "for_device_model",
    type: "name"
  },
  {
    Header: "БРОЙ НАЛИЧНИ",
    accessor: "count",
    type: "name"
  },
  {
    Header: "ЕДИНИЧНА ЦЕНА",
    accessor: "price_per_item",
    type:"name"
  }
]

const mapFunction = (val)=>({
                ...val,
                accessory_type:nameMap(val?.device_type_data?.device_type),
                for_device_type: nameMap(val?.model_data?.device_type_data?.device_type),
                for_device_brand: val?.model_data?.brand_data?.name,
                for_device_model: `${val?.model_data?.model} ${val?.model_data?.modification ?? ""}`,
                count_available: val?.count,
                price_per_item: val?.price_per_item
        })

export const Accessories = () =>{
    return (
        <RenderTable
            url="/accessories/?related=1"
            columns={columns}
            tableName = "Аксесоари"
            mapFunction = {mapFunction}
        />
    )
}