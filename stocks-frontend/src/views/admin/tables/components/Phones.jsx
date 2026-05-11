import {columnsPhones} from "../variables/columnsData";
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
    Header: "ИЗПОЛЗВАН",
    accessor: "phone_status",
    type: "name",
  },
  {
    Header: "МАКСИМАЛНО НИВО НА БАТЕРИЯ",
    accessor: "battery_capacity",
    type: "progress",
  },
  {
    Header: "ВЪТРЕШНА ПАМЕТ",
    accessor: "capacity_gb",
    type: "name",
  },
  {
    Header: "RAM",
    accessor: "RAM",
    type: "name",
  },
    {
    Header: "ЦЕНА",
    accessor: "price",
    type: "quantity",
    },
  {
    Header: "ЗАБЕЛЕЖКИ",
    accessor: "notes",
    type: "name",
  }
];

const mapFunction = (val)=>({
                ...val,
                brand:[val.model_data.brand_data.name||"samsung"],
                model:`${val.model_data.model} ${val.model_data.modification || ''}`,
                phone_status:nameMap(val.phone_status),
                battery_capacity:val.battery_status || 100,
                capacity_gb: val.capacity_gb ? `${val.capacity_gb}Gb` : "",
                RAM:val.RAM ? `${val.RAM}Gb`: "",
                price:`${(val.price).toFixed(2)}€ / ${(val.price * 1.95583).toFixed(2)}лв.`,
                notes:val.notes,
        })

export const Phones = () =>{
    return (
        <RenderTable
            url="/phones/?related=1"
            columns={columns}
            tableName = "Телефони в наличност"
            mapFunction = {mapFunction}
        />
    )
}