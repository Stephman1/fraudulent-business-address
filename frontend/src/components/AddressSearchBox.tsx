import { 
  Form,
  FormControl, 
  FormField, 
  FormItem, 
  FormLabel, 
  FormMessage 
} from "./ui/form"

import { useState } from "react";
import axios from "axios";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import CompanyTable from "./CompanyTable";
import { CompanyDataItem } from "./CompanyTable";
import UserInfoForm from "./UserInfoForm";

import { useForm } from 'react-hook-form'
import * as z from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'


export const Address = z.object({
  streetNo: z.string().toLowerCase().optional(),
  streetName: z.string().min(1, { message: 'Street name is required' }).toLowerCase(),
  postcodePart1: z.string().min(2, { message: 'First part of postcode is at least 2 characters' }).toUpperCase()
    .max(4, { message: 'First part of postcode is at most 4 characters' })
    .refine(value => /^[A-Za-z]/.test(value), { message: 'First part of postcode must start with a letter' }),
  postcodePart2: z.string().length(3, { message: 'Second part of postcode must have 3 characters' }).toUpperCase()
    .refine(value => /^[0-9]/.test(value), { message: 'Second part of postcode must start with a digit' }),
})


const AddressSearchBox = () => {
  const [unionData, setUnionData] = useState<CompanyDataItem[] | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const form = useForm<z.infer<typeof Address>>({
    resolver: zodResolver(Address),
    defaultValues: {
      streetNo: '',
      streetName: '',
      postcodePart1: '',
      postcodePart2: '',
    },
  })

  const onSubmit = async (addressData: any) => {
    console.log('addressData', addressData )
    setIsLoading(true)

    try {
      const encodedStreetName = encodeURIComponent(addressData.streetName);
      const streetNameRequestUrl = `http://127.0.0.1:8000/api/search-address/?query=${encodedStreetName}`
      const encodedPostcode = encodeURIComponent(addressData.postcodePart1 + ' ' +addressData.postcodePart2);

      const streetNameResponse = await axios.get(streetNameRequestUrl, {
        headers: {
          Accept: "application/json",
        },
      })
      const postcodeResponse = await axios
        .get(`http://127.0.0.1:8000/api/search-address/?query=${encodedPostcode}`, {
        headers: {
          Accept: "application/json",
        },
      })
      
      const updated_streetName_data: CompanyDataItem[] = handleResponseData(streetNameResponse.data.items)
      const updated_postcode_data: CompanyDataItem[] = handleResponseData(postcodeResponse.data.items)

      // console.log('updated_postcode_data', updated_postcode_data)
      // console.log('updated_streetName_data', updated_streetName_data)


      // Create a set to track unique company numbers
      const companyNumberSet = new Set<string>();

      // Create an array to hold the merged data
      const mergedData: CompanyDataItem[] = [];

      // Add unique entries from updated_streetName_data
      updated_streetName_data.forEach(item => {
          if (!companyNumberSet.has(item.company_number)) {
              companyNumberSet.add(item.company_number);
              mergedData.push(item);
          }
      });

      // Add unique entries from updated_postcode_data
      updated_postcode_data.forEach(item => {
          if (!companyNumberSet.has(item.company_number)) {
              companyNumberSet.add(item.company_number);
              mergedData.push(item);
          }
      });
        
      setUnionData(mergedData)
      setIsLoading(false)

    } catch (error) {
      console.log(error)
      setIsLoading(false)
    }
  };

  const concatenateAddress = (address: any) => {
    const updatedAddress = `${address.address_line_1 ? address.address_line_1 + ", " : ""}
    ${address.address_line_2 ? address.address_line_2 + ", " : ""}
    ${address.locality ? address.locality + ", " : ""}
    ${address.region ? address.region + ", " : ""}
    ${address.postal_code ? address.postal_code + ", " : ""}`

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
    <div className="w-full flex flex-col justify-center">
      <Form {...form}>
          <form className="grid gap-4 py-5" onSubmit={form.handleSubmit(onSubmit)}>
            <FormField 
              control={form.control}
              name="streetNo"
              render={({ field }) => (
                <FormItem>
                  <div className="grid grid-cols-4 items-center gap-6">
                    <FormLabel className="text-right">Street no/House name</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="26" 
                        className="col-span-2" 
                        {...field} />
                    </FormControl>
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField 
              control={form.control}
              name="streetName"
              render={({ field }) => (
                <FormItem>
                  <div className="grid grid-cols-4 items-center gap-6">
                    <FormLabel className="text-right">Street</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="Baker Street" 
                        className="col-span-2" 
                        {...field} />
                    </FormControl>
                  </div>
                  <FormMessage className="text-right" />
                </FormItem>
              )}
            />
            <div className="grid grid-cols-4 items-center gap-6">
              <FormLabel className="text-right">Postcode</FormLabel>
                <FormField
                  control={form.control}
                  name="postcodePart1"
                  render={({ field }) => (
                    <FormItem className="col-span-1">
                      <FormControl>
                        <Input placeholder="WC1B" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="postcodePart2"
                  render={({ field }) => (
                    <FormItem className="col-span-1">
                      <FormControl>
                        <Input placeholder="3DG" {...field} />
                      </FormControl>
                      <FormMessage className="text-right"/>
                    </FormItem>
                  )}
                />
            </div>
          </form>
          <div className="grid grid-cols-8 items-center gap-6">
            <Button
              type="submit"
              className="col-start-5 bg-gradient-to-r from-green-500 to-blue-500 hover:from-pink-500 hover:to-yellow-500"
              onClick={form.handleSubmit(onSubmit)}
            >
              Search
            </Button>
            <UserInfoForm />
          </div>
        </Form>
      
      {isLoading ? (
        <CompanyTable.Skeleton />
      ) : unionData && unionData.length > 0 ? (
        <CompanyTable items={unionData} />
      ) : (
          !isLoading && unionData && unionData.length === 0 && 
          <p className="text-center mt-8 font-semibold text-orange-950">
            There are currently no companies registered at this address
          </p>
      )}
    </div>
  );
};

export default AddressSearchBox;
