import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { 
  Form, 
  FormControl, 
  FormField, 
  FormItem, 
  FormLabel, 
  FormMessage 
} from "./ui/form"
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

 
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { ChevronsUpDown } from "lucide-react"

import * as z from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import axios from "axios"
import { toast } from 'sonner'


export const User = z.object({
  email: z.string().min(1, { message: 'Email is required' }).email({ message: 'Invalid email address' }).toLowerCase(),
  streetNo: z.string().toLowerCase().optional(),
  streetName: z.string().min(1, { message: 'Street name is required' }).toLowerCase(),
  postcodePart1: z.string().min(2, { message: 'First part of postcode is at least 2 characters' }).toUpperCase()
    .max(4, { message: 'First part of postcode is at most 4 characters' })
    .refine(value => /^[A-Za-z]/.test(value), { message: 'First part of postcode must start with a letter' }),
  postcodePart2: z.string().length(3, { message: 'Second part of postcode must have 3 characters' }).toUpperCase()
    .refine(value => /^[0-9]/.test(value), { message: 'Second part of postcode must start with a digit' }),
  existingBusinesses: z.preprocess((val) => val === '' ? undefined : Number(val), 
  z.number({ 
    invalid_type_error: "Please enter a number" 
  }).nonnegative().finite()),
  additionalAddress: z.string().toLowerCase(),
})

const UserInfoForm = () => {

  const [open, setOpen] = useState(false)
  const [isCollapsed, setIsCollapsed] = useState(false)

  const form = useForm<z.infer<typeof User>>({
    resolver: zodResolver(User),
    defaultValues: {
      email: '',
      streetNo: '',
      streetName: '',
      postcodePart1: '',
      postcodePart2: '',
      existingBusinesses: 0,
      additionalAddress: 'no'
    },
  })
  
  async function onSubmit(userData: any) {

    console.log('submitting', userData)
    handleClose()
    form.reset()

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/add-user-data/', userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.status === 201) {
        toast.success(`New user ${userData.email} and address have been created successfully!`, {duration: 8000})
        console.log('User created successfully:', response.data)
      } 
      
    } catch (error: any) {
      if (error.response && error.response.status === 400) {
        toast.error('User email and address already exist! Please use a different email or address.', { duration: 8000 });
        console.log('Error:', error.response.data)
      } else {
          toast.error('An unexpected error occurred. Please try again later.', { duration: 8000 });
          console.log('Unexpected Error:', error)
      } 
    }
  }
  
  const handleOpen = () => {
    form.reset()
    setOpen(true)
  }
    
  const handleClose = () => {
    setOpen(false)
    form.reset()
  } 

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button 
          type="submit"
          variant="outline" 
          onClick={handleOpen}
          className="text-white bg-gradient-to-r from-blue-500 to-green-500
           hover:from-yellow-500 hover:to-pink-500 hover:text-white"
        >
          Notify me
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle>Edit User Info</DialogTitle>
          <DialogDescription>
            Save your user info to get notified when new businesses are registered at your address
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form className="grid gap-4 py-5" onSubmit={form.handleSubmit(onSubmit)}>
            <FormField 
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <div className="grid grid-cols-3 items-center gap-6">
                    <FormLabel className="text-right">Email</FormLabel>
                    <FormControl>
                      <Input placeholder="example@gmail.com" className="col-span-2" {...field} />
                    </FormControl>
                  </div>
                  <FormMessage className="text-right"/>
                </FormItem>
              )}
            />
            <FormField 
              control={form.control}
              name="streetNo"
              render={({ field }) => (
                <FormItem>
                  <div className="grid grid-cols-3 items-center gap-6">
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
                  <div className="grid grid-cols-3 items-center gap-6">
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
            <div className="grid grid-cols-3 items-center gap-6">
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
            <Collapsible
              open={isCollapsed}
              onOpenChange={setIsCollapsed}
              className="space-y-2"
            >
              <div className="flex items-center justify-center space-x-4 px-4">
                <CollapsibleTrigger asChild>
                  <Button variant="ghost" size="sm" className="w-9 p-0">
                    <ChevronsUpDown className="h-4 w-4" />
                    <span className="sr-only">Toggle</span>
                  </Button>
                </CollapsibleTrigger>
              </div>
              <CollapsibleContent className="space-y-2">
                <FormField 
                  control={form.control}
                  name="existingBusinesses"
                  render={({ field }) => (
                    <FormItem className="grid gap-5">
                      <div className="grid grid-cols-3 items-center gap-6">
                        <FormLabel>
                          <TooltipProvider delayDuration={0}>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="outline">Existing businesses</Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p className="text-sky-950">
                                  How many existing businesses do you have registered at this address?
                                </p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        </FormLabel>
                        <FormControl>
                          <Input 
                            type="number" 
                            placeholder="0" 
                            className="col-span-2"
                            min={0}
                            {...field} 
                          />
                        </FormControl>
                      </div>
                      <FormMessage className="text-right"/>
                    </FormItem>
                  )}
                />
                <FormField 
                  control={form.control}
                  name="additionalAddress"
                  render={({ field }) => (
                    <FormItem className="grid">
                      <div className="grid grid-cols-3 items-center gap-6">
                        <FormLabel>
                          <TooltipProvider delayDuration={0}>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button variant="outline">Additional address</Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p className="text-sky-950">
                                  Is this an additional residential address?
                                </p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        </FormLabel>
                        <Select onValueChange={field.onChange}>
                          <FormControl className="col-span-2">
                            <SelectTrigger >
                              <SelectValue placeholder="No" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="no">No</SelectItem>
                            <SelectItem value="yes">Yes</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <FormMessage className="text-right"/>
                    </FormItem>
                  )}
                />
              </CollapsibleContent>
            </Collapsible>
          </form>
          <DialogFooter >
            <Button 
              type="submit" 
              onClick={form.handleSubmit(onSubmit)}
            >
              Save changes
            </Button>
          </DialogFooter>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default UserInfoForm