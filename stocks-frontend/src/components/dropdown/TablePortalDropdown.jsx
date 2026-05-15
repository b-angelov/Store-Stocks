import React, { useState, useRef, useEffect } from "react";
import { createPortal } from "react-dom";

function TablePortalDropdown({values, placeholder, label, selectFn}) {
    const [isOpen, setIsOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [coords, setCoords] = useState({ top: 0, left: 0, width: 0 });

    const inputContainerRef = useRef(null);
    values = values || [];
    selectFn = selectFn || (e=>e)


    const updatePosition = () => {
        if (inputContainerRef.current) {
            const rect = inputContainerRef.current.getBoundingClientRect();
            setCoords({
                top: rect.top + 45,
                left: rect.left,
                width: rect.width,
            });
        }
    };

    useEffect(() => {
        if (isOpen) {
            updatePosition();
            window.addEventListener("scroll", updatePosition, true);
            window.addEventListener("resize", updatePosition);
        }
        return () => {
            window.removeEventListener("scroll", updatePosition, true);
            window.removeEventListener("resize", updatePosition);
        };
    }, [isOpen]);

    return (
      <div className="w-full">
        <div
          ref={inputContainerRef}
          className="flex h-10 w-1/4 items-center rounded-xl bg-lightPrimary p-2 dark:bg-navy-700"
        >
          <input
            type="text"
            placeholder={placeholder}
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              !e.target.value && selectFn(e, {search: false});
            }}
            onFocus={() => setIsOpen(true)}
            onBlur={() => setTimeout(() => setIsOpen(false), 200)}
            className="bg-transparent h-full w-full text-sm font-medium text-navy-700 outline-none dark:text-white"
          />
        </div>

        {isOpen &&
          createPortal(
            <div
              style={{
                position: "fixed",
                top: `${coords.top}px`,
                left: `${coords.left}px`,
                width: `${coords.width}px`,
              }}
              className="z-[9999] flex max-h-[240px] flex-col overflow-y-auto rounded-[20px] border border-gray-100 bg-white p-3 shadow-xl shadow-shadow-500 dark:border-none dark:!bg-navy-800"
            >
              {values
                .filter((v) =>
                  v?.display?.toLowerCase().includes(searchTerm.toLowerCase())
                )
                .map((value) => (
                  <button
                    key={value?.display}
                    onMouseDown={(e) => {
                      e.preventDefault();
                      setSearchTerm(
                        value?.display === "all" ? "" : value?.display
                      );
                      selectFn(e,value);
                      setIsOpen(false);
                    }}
                    className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-left text-sm capitalize text-gray-700 hover:bg-gray-50 dark:text-gray-200 dark:hover:bg-navy-700"
                  >
                    {/*<img*/}
                    {/*    src={brand === "all" ? "https://logo.dev" : `https://logo.dev{brand}.com`}*/}
                    {/*    alt={brand}*/}
                    {/*    className="w-5 h-5 object-contain"*/}
                    {/*    onError={(e) => { e.target.src = "https://logo.dev"; }}*/}
                    {/*/>*/}
                    {value?.display}
                  </button>
                ))}
            </div>,
            document.body
          )}
      </div>
    );
}

export default TablePortalDropdown;
