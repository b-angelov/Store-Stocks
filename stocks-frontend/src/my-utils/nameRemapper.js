
export const nameMap = (val) => ({
    "iphone":"apple",
        "old": "Стар",
        "new":"Нов",
        "windows":"microsoft",
        "cases": "калъфи",
        "phones": "смартфони",
        "phone": "смартфон",
        "wallet cases": "тефтери",
        "screen protector": "екранни протектори",
        "all": "alphabet",
}[val?.toLowerCase()] ?? val
)