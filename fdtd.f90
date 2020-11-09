program fdtd
    implicit none
    integer, parameter :: length=120
    ! real, parameter :: c0=299792458.
    real, dimension(length) :: epsilon_r, mu_r, mE, mH, Ey, Hx
    real :: dz=1
    integer :: k, step, steps_per_frame=6, frame, number_of_frames=60
    character(len=20) :: filename1, filename2, format_string='(E16.9)'
    
    ! Initialize materials to free space
    ! Initialize fields to zero
    do k=1, length
        epsilon_r(k)=1
        mu_r(k)=1

        Hx(k)=0
        Ey(k)=0
    end do

    Hx(40)=1
    
    ! Compute update coefficients

    ! dt = n*dz/(2*c0)
    ! n := refractive index at boundries
    ! mE = c0*dt/epsilon_r = n*dz/(2*epsilon_r)
    ! mH = c0*dt/mu_r = n*dz/(2*mu_r)

    mE = 0.5/epsilon_r
    mH = 0.5/mu_r

    ! Main FDTD loop
    do frame = 1, number_of_frames
        
        write (filename1,'("./output/Hx"I4.4".csv")') frame
        open(1, file=filename1, status='replace')
        do k = 1, length-1
            write(1,format_string,advance='NO') Hx(k)
            write(1,'(A)',advance='NO') ','
        end do
        write(1,format_string,advance='NO') Hx(length)
        close(1)

        write (filename2,'("./output/Ey"I4.4".csv")') frame
        open(2, file=filename2, status='replace')
        write(2,format_string,advance='NO') Ey(1)
        do k = 2, length
            write(2,'(A)',advance='NO') ','
            write(2,format_string,advance='NO') Ey(k)
        end do
        close(2)

        do step = 1, steps_per_frame
            
            do k = 1, length-1
                Hx(k) = Hx(k) + mH(k)*(Ey(k+1)-Ey(k))/dz
            end do
            Hx(length) = Hx(length) - mH(length)*Ey(length)/dz

            Ey(1) = Ey(1) + mE(1)*Hx(1)/dz
            do k = 2, length
                Ey(k) = Ey(k) + mE(k)*(Hx(k)-Hx(k-1))/dz
            end do

        end do

    end do


end program fdtd