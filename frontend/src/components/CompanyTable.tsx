import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableFooter,
  TableRow,
} from "./ui/table"
import { Skeleton } from './ui/skeleton'
export interface CompanyDataItem {
  company_name: string,
  company_number: string,
  company_status: string,
  company_type: string,
  date_of_creation: string,
  registered_office_address?: string
  full_address?: string,
}


interface CompanyTableProps {
  items: CompanyDataItem[]
}


const CompanyTable = (data: CompanyTableProps) => {
  return (
    <Table className='mt-10 w-full table-fixed border-collapse overflow-x-auto'>
    <TableHeader>
      <TableRow>
        <TableHead className="text-left whitespace-nowrap">Company Number</TableHead>
        <TableHead className="text-left whitespace-nowrap">Company Name</TableHead>
        <TableHead className="text-left whitespace-nowrap">Company Status</TableHead>
        <TableHead className="text-left whitespace-nowrap">Company Type</TableHead>
        <TableHead className="text-left whitespace-nowrap">Date of Creation</TableHead>
        <TableHead className="text-left whitespace-nowrap">Registered Address</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
    {data.items.map((company) => (
      <TableRow key={company.company_number}>
        <TableCell className="font-medium">{company.company_number}</TableCell>
        <TableCell className="text-left text-sky-950 whitespace-wrap">{company.company_name}</TableCell>
        <TableCell className="text-center text-sky-950 whitespace-wrap">{company.company_status}</TableCell>
        <TableCell className="text-center text-sky-950 whitespace-wrap">{company.company_type}</TableCell>
        <TableCell className="text-left text-sky-950 whitespace-wrap">{company.date_of_creation}</TableCell>
        <TableCell className="text-left text-sky-950 overflow text-ellipsis whitespace-nowrap">{company.full_address}</TableCell>
      </TableRow>
    ))}
    </TableBody>
    <TableFooter>
        <TableRow>
          <TableCell className="text-left" colSpan={5}>Total Number of Companies</TableCell>
          <TableCell className="text-right">{data.items.length}</TableCell>
        </TableRow>
      </TableFooter>
  </Table>
  )
}

CompanyTable.Skeleton = () => {
  return (
    <Table className='mt-10 w-full'>
      <TableBody className='space-y-3'>
        <Skeleton className="bg-gray-200 rounded-md h-20 w-full"/>
        <div className="space-y-2">
          <Skeleton className="bg-gray-200 h-4 w-[70%]"/>
          <Skeleton className="bg-gray-200 h-4 w-[80%]"/>
        </div>
      </TableBody>
    </Table>
  )
}

export default CompanyTable


