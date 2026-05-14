import {columnsPhones} from "../variables/columnsData";
import {RenderTable} from "./RenderTable";
import {nameMap} from "../../../../my-utils/nameRemapper";
import InputField from "../../../../components/fields/InputField";
import Card from "../../../../components/card";
import {MdOutlineSmartphone} from "react-icons/md";
import {useState} from "react";
import Dropdown from "../../../../components/dropdown";

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

const brandsColumns = [
     {
    Header: "НАЛИЧНИ МАРКИ ТЕЛЕФОНИ",
    accessor: "name",
    type: "vendor",
  },
]

const brandMapFn = (val) =>({
    ...val
})


export const Phones = () =>{

    const [filters, setFilters] = useState({
        brandFilter: false,
    })

    const preProcessDataFn = (data) =>([
        {name: ["all"].concat(data.map(brand=>brand.name))}
    ])

    return (
      <>
        <RenderTable
          url={"/phones/brands/?related=1"}
          columns={brandsColumns}
          tableName={"НАЛИЧНИ МАРКИ"}
          mapFunction={brandMapFn}
          preProcessDataFn={preProcessDataFn}
          columnParams={{
            titleBelow: true,
            vendorOnClick: (e, params, item) => {
              // e.stopPropagation();
              setFilters((old) => ({
                ...old,
                brandFilter: item == "all" ? false : item,
              }));
            },
          }}
        >
          <Dropdown
            // 1. Подаваме задействащия елемент (бутон или input)
            button={
              <InputField
                placeholder={"Налични модели"}
                classNames={
                  "rounded-xl bg-lightPrimary p-3 text-sm font-medium text-navy-700 outline-none dark:bg-navy-800 dark:text-white w-64"
                }
              />
            }
            // 2. Позициониране и анимация
            classNames="!left-0 !right-auto top-12 left-0 w-64"
            animation="origin-top-left transition-all duration-300 ease-in-out"
          >
            <div className=" mt-4 rounded-[20px] bg-white p-4 shadow-xl dark:bg-navy-700">
              My thing
            </div>
          </Dropdown>
        </RenderTable>

        <RenderTable
          url={
            "/phones/?related=1" +
            (filters?.brandFilter ? `&of_brand=${filters.brandFilter}` : "")
          }
          columns={columns}
          tableName="Телефони в наличност"
          mapFunction={mapFunction}
        />
      </>
    );
}