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
import { Input } from "@/components/ui/input"
import { useState } from "react"

import * as z from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import axios, { AxiosError, AxiosPromise, AxiosResponse } from "axios"
import { toast } from 'sonner'



export const User = z.object({
  email: z.string().min(1, { message: 'Email is required' }).email({ message: 'Invalid email address' }),
  address: z.string().min(1, { message: 'Address is required' }),
  city: z.string().min(1, { message: 'City is required' }),
  postcode: z.string().min(1, { message: 'Postcode is required' }),
  count: z.preprocess((val) => val === '' ? undefined : Number(val), 
  z.number({ 
    required_error: "Count is required", 
    invalid_type_error: "Please enter a number" 
  }).nonnegative().finite()),
});

const UserInfoForm = () => {

  const [open, setOpen] = useState(false)

  const [userInfo, setUserInfo] = useState<z.infer<typeof User>>({
    email: '',
    address: '',
    city: '',
    postcode: '',
    count: 0
  })

  const form = useForm<z.infer<typeof User>>({
    resolver: zodResolver(User),
    defaultValues: {
      email: '',
      address: '',
      city: '',
      postcode: '',
    },
  })
  
  async function onSubmit(userData: z.infer<typeof User>) {
    console.log('submitting', userData)
    setUserInfo(userData)
    handleClose()
    form.reset()

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/add-user-data/', userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (response.status === 201) {
        toast.success(`New user ${userData.email} has been created successfully!`, {duration: 8000})
        console.log('User created successfully:', response.data);
      } 
      
    } catch (error: any) {
      if (error.response && error.response.status === 400) {
        toast.error('User email already exists! Please use a different email.', { duration: 8000 });
        console.log('Error:', error.response.data);
      } else {
          toast.error('An unexpected error occurred. Please try again later.', { duration: 8000 });
          console.log('Unexpected Error:', error);
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
      <DialogContent className="sm:max-w-[425px]">
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
                  <div className="grid grid-cols-5 items-center gap-5">
                    <FormLabel className="text-right">Email</FormLabel>
                    <FormControl>
                      <Input placeholder="example@gmail.com" className="col-span-4" {...field} />
                    </FormControl>
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField 
              control={form.control}
              name="address"
              render={({ field }) => (
                <FormItem>
                  <div className="grid grid-cols-5 items-center gap-5">
                    <FormLabel className="text-right">address</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="Great Russell St" 
                        className="col-span-4" 
                        {...field} />
                    </FormControl>
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField 
              control={form.control}
              name="city"
              render={({ field }) => (
                <FormItem>
                  <div className="grid grid-cols-5 items-center gap-5">
                    <FormLabel className="text-right">city</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="London" 
                        className="col-span-4" 
                        {...field} />
                    </FormControl>
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField 
              control={form.control}
              name="postcode"
              render={({ field }) => (
                <FormItem>
                  <div className="grid grid-cols-5 items-center gap-2">
                    <FormLabel className="text-right">postcode</FormLabel>
                    <FormControl>
                      <Input 
                        placeholder="WC1B 3DG" 
                        className="col-span-4" 
                        {...field} />
                    </FormControl>
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField 
              control={form.control}
              name="count"
              render={({ field }) => (
                <FormItem className="grid gap-5">
                  <div className="grid grid-cols-5 items-center gap-5">
                    <FormLabel>
                      <TooltipProvider delayDuration={0}>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button variant="outline">Count</Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p className="text-sky-950">
                              How many of your businesses are currently registered at this address?
                            </p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    </FormLabel>
                    <FormControl>
                      <Input 
                        type="number" 
                        placeholder="0" 
                        className="col-span-4"
                        min={0}
                        {...field} 
                      />
                    </FormControl>
                  </div>
                  <FormMessage />
                </FormItem>
              )}
            />
          </form>
          <DialogFooter>
            <Button 
              type="submit" 
              onClick={form.handleSubmit(onSubmit)}>Save changes</Button>
          </DialogFooter>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default UserInfoForm