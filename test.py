def test():
    """
    demonstrates basic pygrib functionality.

    open a grib file, create an iterator.
    >>> import pygrib
    >>> grbs = pygrib.open('sampledata/flux.grb')

    iterate over all grib messages.
    >>> for grb in grbs: print grb
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120:from 200402291200
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200

    iterator now positioned at last message
    >>> print grb
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200

    position iterator at beginning again.
    >>> grbs.rewind() 
    >>> for grb in grbs: print grb
    1:Precipitation rate:kg m**-2 s**-1 (avg):regular_gg:surface:level 0:fcst time 108-120:from 200402291200
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200

    get a specific grib message from the iterator.
    iterator will be positioned at this message.
    >>> grb = grbs.message(2) 
    >>> print grb # 2nd message
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200

    position iterator at next grib message.
    >>> grb = grbs.next() 
    >>> print grb # 3rd message
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200

    now the iterator should be positioned at the last (4th) message.
    >>> for grb in grbs: print grb # only last message printed.
    4:Minimum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200

    rewind again
    >>> grbs.rewind()

    iterate over all messages until
    'Maximum temperature' is found.
    >>> for grb in grbs:
    ...     if grb['name'] == 'Maximum temperature': break
    ...
    >>> print grb
    3:Maximum temperature:K (instant):regular_gg:heightAboveGround:level 2:fcst time 108-120:from 200402291200

    get the data and the lat/lon values of the Max temp grid 
    >>> data = grb['values'] # 'values' returns the data
    >>> print '-- data values, grid info for msg number %d --' % grb.messagenumber
    -- data values, grid info for msg number 3 --
    >>> print 'shape/min/max data %s %6.2f %6.2f'%(str(data.shape),data.min(),data.max())
    shape/min/max data (94, 192) 223.70 319.90
    >>> lats, lons = grb.latlons() # returns lat/lon values on grid.
    >>> print 'min/max of %d lats on %s grid %4.2f %4.2f' % (grb['Nj'], grb['typeOfGrid'],lats.min(),lats.max())
    min/max of 94 lats on regular_gg grid -88.54 88.54
    >>> print 'min/max of %d lons on %s grid %4.2f %4.2f' % (grb['Ni'], grb['typeOfGrid'],lons.min(),lons.max())
    min/max of 192 lons on regular_gg grid 0.00 358.12

    get 2nd grib message
    >>> grb = grbs.message(2)
    >>> print grb
    2:Surface pressure:Pa (instant):regular_gg:surface:level 0:fcst time 120:from 200402291200
    >>> print 'valid date',grb['validityDate']
    valid date 20040305
    >>> print 'min/max %5.1f %5.1f' % (grb['minimum'],grb['maximum'])
    min/max 49650.0 109330.0

    change the forecast time
    >>> grb['forecastTime'] = 240  
    >>> grb['parameterNumber'] = 2 # change to pressure tendency
    >>> data = grb['values']
    >>> grb['values']=data/86400. # put in units of Pa/S

    open an output file for writing
    >>> grbout = open('test.grb','w')

    get coded binary string for modified message
    >>> msg = grb.tostring()

    write to file and close.
    >>> grbout.write(msg)
    >>> grbout.close()

    reopen file, check contents.
    >>> grbs = pygrib.open('test.grb')
    >>> grb = grbs.next()
    >>> print grb
    1:Pressure tendency:Pa s**-1 (instant):regular_gg:surface:level 0:fcst time 240:from 200402291200
    >>> print 'valid date',grb['validityDate']
    valid date 20040310
    >>> print 'min/max %4.2f %4.2f' % (grb['minimum'],grb['maximum'])
    min/max 0.57 1.27
    >>> grbs.close()
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
