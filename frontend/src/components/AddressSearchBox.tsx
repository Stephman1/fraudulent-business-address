import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useState } from "react";
import axios from "axios";
import CompanyTable from "./CompanyTable";
import { CompanyDataItem } from "./CompanyTable";


const AddressSearchBox = () => {
  const [query, setQuery] = useState("");
  const [data, setData] = useState<CompanyDataItem[] | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    event.preventDefault();
    setQuery(event.target.value);
  };

  const handleSubmit = async (
    event:
      | React.MouseEvent<HTMLButtonElement>
      | React.KeyboardEvent<HTMLInputElement>
  ) => {
    event.preventDefault();

    setIsLoading(true)

    try {
      const encodedQuery = encodeURIComponent(query);
      
      const requestUrl = `http://127.0.0.1:8000/api/company-data/?query=${encodedQuery}`;
      const response = await axios.get(requestUrl, {
        headers: {
          Accept: "application/json",
        },
      })
      
      const updated_data: CompanyDataItem[] = handleResponseData(response.data.items)
        
      setData(updated_data)
      setIsLoading(false)

    } catch (error) {
      console.log(error);
      setIsLoading(false)
    }
    setQuery("");
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      handleSubmit(event);
    }
  };

  const concatenateAddress = (address: any) => {
    const updatedAddress = `${address.address_line_1 ? address.address_line_1 + ", " : ""}${address.address_line_2 ? address.address_line_2 + ", " : ""}${address.locality ? address.locality + ", " : ""}${address.region ? address.region + ", " : ""}${address.postal_code ? address.postal_code + ", " : ""}`

    if (updatedAddress.slice(-2) == ', ') {
      return updatedAddress.slice(0, -2)
    } else {
      return updatedAddress
    }
  };

  function handleResponseData(responseData: any[]): CompanyDataItem[] {
    if (responseData == undefined) {
      return []
    }

    const transformedData: CompanyDataItem[] = responseData.map((item: any) => {
      const address = item.registered_office_address;
      item.full_address = concatenateAddress(address);
      return {
        company_name: item.company_name,
        company_number: item.company_number,
        company_status: item.company_status,
        company_type: item.company_type,
        date_of_creation: item.date_of_creation,
        registered_office_address: item.registered_office_address,
        full_address: item.full_address
      };
    });

    return transformedData;
  };

  return (
    <div className="w-full">
      <div className="flex flex-row justify-center items-center gap-4 m-2 w-full">
        <Input
          type="text"
          placeholder="Address"
          className="h-10 flex-grow input input-bordered border-rounded"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
        />
        <Button
          type="submit"
          className="bg-gradient-to-r from-green-400 to-blue-500 hover:from-pink-500 hover:to-yellow-500"
          onClick={handleSubmit}
        >
          Search
        </Button>
      </div>
        
      {isLoading ? (
        <CompanyTable.Skeleton />
      ) : data && data.length > 0 ? (
        <CompanyTable items={data} />
      ) : (
          !isLoading && data && data.length === 0 && <p className="text-center mt-8 font-semibold text-orange-950">There are no companies registered under this address</p>
      )}
    </div>
  );
};

export default AddressSearchBox;
